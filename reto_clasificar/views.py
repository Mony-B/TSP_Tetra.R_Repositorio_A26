"""
Clasificar elementos por categorías (CU-08).

Todo se evalúa en el servidor: la categoría correcta de cada ficha nunca llega
al navegador. Las fichas ya bien clasificadas se guardan en la sesión mientras
se juega; si el alumno sale o recarga, empieza desde cero (el reto solo tiene
dos estados: completado o no). Al clasificar la última ficha se registra el
reto con progreso, que da los bitcoins solo la primera vez.
"""
import json

from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from mapa.temas import materia_de_reto
from progreso import servicios

from .ejercicios import EJERCICIOS, datos_publicos, evaluar_ficha, fichas, verificar_completo

APP = "reto_clasificar"


def _ejercicio(ejercicio_id):
    if ejercicio_id not in EJERCICIOS:
        raise Http404("Ejercicio no encontrado")
    return EJERCICIOS[ejercicio_id]


def _json(request):
    try:
        datos = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return None
    return datos if isinstance(datos, dict) else None


# --- Estado de la partida (en la sesión) ------------------------------------------

def _clave_sesion(clave):
    return f"clasificar:{clave}"


def _clasificadas(request, clave):
    """Ids de las fichas ya bien clasificadas (valida lo que viene de la sesión)."""
    guardadas = request.session.get(_clave_sesion(clave))
    if not isinstance(guardadas, list):
        return []
    return [f for f in guardadas if isinstance(f, str)]


def _reiniciar(request, clave):
    request.session.pop(_clave_sesion(clave), None)
    servicios.reiniciar_pasos(request, clave)


# --- Vistas -------------------------------------------------------------------------

@login_required
@ensure_csrf_cookie
def jugar(request, ejercicio_id):
    """Paso 1: enunciado, gráfica, fichas y áreas de destino, más Salir / Rendirse."""
    ejercicio = _ejercicio(ejercicio_id)
    clave = f"{APP}:{ejercicio_id}"
    _reiniciar(request, clave)  # siempre se empieza desde cero
    materia = materia_de_reto(APP, ejercicio_id)
    return render(request, f"{APP}/reto.html", {
        "nombre_reto": "Clasificar por categorías",
        "ejercicio": ejercicio,
        "datos_publicos": datos_publicos(ejercicio_id),
        "revisar_url": reverse(f"{APP}:completar", args=[ejercicio_id]),
        "clasificar_url": reverse(f"{APP}:clasificar", args=[ejercicio_id]),
        "volver_url": reverse("mapa:materia", args=[materia["slug"]]) if materia else reverse("mapa:inicio"),
        "ya_resuelto": servicios.reto_resuelto(request.user, clave),
    })


@login_required
@require_POST
def clasificar(request, ejercicio_id):
    """Pasos 4-5 (FA-1): recibe {"ficha": "f0", "categoria": "si"} y contesta
    { correcto, puntos, total }. Una clasificación incorrecta no es un error
    HTTP: la ficha simplemente regresa al panel y no cambia nada."""
    ejercicio = _ejercicio(ejercicio_id)
    clave = f"{APP}:{ejercicio_id}"
    datos = _json(request)
    if datos is None:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    ficha_id, categoria = str(datos.get("ficha", "")), str(datos.get("categoria", ""))
    correcto = evaluar_ficha(ejercicio, ficha_id, categoria)
    if correcto is None:
        return JsonResponse({"error": "Ficha o categoría inválida"}, status=400)

    clasificadas = _clasificadas(request, clave)
    if correcto and ficha_id not in clasificadas:
        clasificadas.append(ficha_id)
        request.session[_clave_sesion(clave)] = clasificadas
    return JsonResponse({
        "correcto": correcto,
        "puntos": len(clasificadas),
        "total": len(fichas(ejercicio)),
    })


@login_required
@require_POST
def completar(request, ejercicio_id):
    """Pasos 7-8: se llama al clasificar la última ficha. Comprueba en el
    servidor que de verdad estén todas y registra el reto.

    Respuesta: { correcto, completado, mensaje, bitcoins_otorgados,
                 bitcoins_total, ya_otorgado (solo si correcto) }
    """
    ejercicio = _ejercicio(ejercicio_id)
    clave = f"{APP}:{ejercicio_id}"
    if not verificar_completo(ejercicio, _clasificadas(request, clave)):
        return JsonResponse({"error": "Aún quedan fichas por clasificar"}, status=400)

    # progreso registra el reto y da los bitcoins solo la primera vez.
    resultado = servicios.procesar_paso(request, clave, 0, True, 1, ejercicio["bitcoins"])
    resultado["ya_otorgado"] = resultado["bitcoins_otorgados"] == 0
    resultado["mensaje"] = "¡Reto completado!"
    request.session.pop(_clave_sesion(clave), None)
    return JsonResponse(resultado)