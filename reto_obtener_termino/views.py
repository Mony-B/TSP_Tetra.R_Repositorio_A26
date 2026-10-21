"""
El término oculto (CU-09), estilo Wordle. Todo se revisa en el servidor:
el término, su significado y los intentos usados nunca dependen del JS.

Los intentos usados se guardan en la sesión mientras se juega; si el alumno
sale o recarga, el reto empieza desde cero (el reto solo tiene dos estados:
completado o no completado). Al descifrarlo se registra con progreso, que da
los bitcoins solo la primera vez.
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

from .ejercicios import EJERCICIOS, datos_publicos, revisar_intento, validar_intento

APP = "reto_obtener_termino"


def _ejercicio(ejercicio_id):
    if ejercicio_id not in EJERCICIOS:
        raise Http404("Ejercicio no encontrado")
    return EJERCICIOS[ejercicio_id]


# --- Intentos de la partida actual (en la sesión) ---------------------------

def _clave_sesion(clave):
    return f"termino:{clave}"


def _estado(request, clave):
    return request.session.get(_clave_sesion(clave), {"usados": 0, "terminado": False})


def _guardar_estado(request, clave, estado):
    request.session[_clave_sesion(clave)] = estado


def _reiniciar_estado(request, clave):
    request.session.pop(_clave_sesion(clave), None)
    servicios.reiniciar_pasos(request, clave)


# --- Vistas -------------------------------------------------------------------

@login_required
@ensure_csrf_cookie
def jugar(request, ejercicio_id):
    ejercicio = _ejercicio(ejercicio_id)
    clave = f"{APP}:{ejercicio_id}"
    _reiniciar_estado(request, clave)  # siempre se empieza desde cero
    materia = materia_de_reto(APP, ejercicio_id)
    return render(request, f"{APP}/reto.html", {
        "nombre_reto": "Descifrar el término",
        "ejercicio": ejercicio,
        "datos_publicos": datos_publicos(ejercicio),
        "revisar_url": reverse(f"{APP}:revisar", args=[ejercicio_id]),
        "reiniciar_url": reverse(f"{APP}:reiniciar", args=[ejercicio_id]),
        "volver_url": reverse("mapa:materia", args=[materia["slug"]]) if materia else reverse("mapa:inicio"),
        "ya_resuelto": servicios.reto_resuelto(request.user, clave),
    })


@login_required
@require_POST
def revisar(request, ejercicio_id):
    """Recibe {"respuesta": "PALABRA"} y contesta con los colores de cada letra.

    Respuesta: { colores, correcto, completado, intentos_restantes, agotado,
                 mensaje, bitcoins_otorgados, bitcoins_total,
                 significado (solo al descifrarlo), ya_otorgado }
    """
    ejercicio = _ejercicio(ejercicio_id)
    clave = f"{APP}:{ejercicio_id}"
    try:
        datos = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    estado = _estado(request, clave)
    if estado["terminado"] or estado["usados"] >= ejercicio["intentos"]:
        return JsonResponse({"error": "No quedan intentos. Presiona Reintentar."}, status=400)

    intento, error = validar_intento(ejercicio, datos.get("respuesta", ""))
    if error:
        # Un intento mal formado no gasta intentos.
        return JsonResponse({"error": error}, status=400)

    colores, correcto = revisar_intento(ejercicio, intento)
    estado["usados"] += 1
    restantes = ejercicio["intentos"] - estado["usados"]
    estado["terminado"] = correcto or restantes == 0
    _guardar_estado(request, clave, estado)

    # progreso registra el reto y da los bitcoins solo la primera vez.
    resultado = servicios.procesar_paso(request, clave, 0, correcto, 1, ejercicio["bitcoins"])
    resultado.update({
        "intento": intento,
        "colores": colores,
        "intentos_restantes": restantes,
        "agotado": not correcto and restantes == 0,
    })
    if correcto:
        resultado["significado"] = ejercicio["significado"]
        resultado["ya_otorgado"] = resultado["bitcoins_otorgados"] == 0
        resultado["mensaje"] = "¡Término descifrado!"
    elif restantes == 0:
        resultado["mensaje"] = "Se agotaron los intentos. No obtuviste bitcoins."
    else:
        resultado["mensaje"] = f"Ese no es el término. Te quedan {restantes} intento(s)."
    return JsonResponse(resultado)


@login_required
@require_POST
def reiniciar(request, ejercicio_id):
    """Botón Reintentar (FA-1): restablece los intentos y la cuadrícula."""
    ejercicio = _ejercicio(ejercicio_id)
    _reiniciar_estado(request, f"{APP}:{ejercicio_id}")
    return JsonResponse({"intentos_restantes": ejercicio["intentos"]})
