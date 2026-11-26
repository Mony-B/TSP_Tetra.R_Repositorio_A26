"""
Tiro parabólico (CU-12). El ángulo y la fuerza se validan y la trayectoria
se calcula en el servidor; el navegador solo anima con los coeficientes que
recibe. Los intentos usados se guardan en la sesión mientras se juega; si el
alumno sale o recarga, empieza desde cero (el reto solo tiene dos estados:
completado o no). Al impactar se registra con progreso, que da los bitcoins
solo la primera vez.
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

from .ejercicios import EJERCICIOS, calcular_disparo, datos_publicos, validar_rango

APP = "reto_parabolica"


def _ejercicio(ejercicio_id):
    if ejercicio_id not in EJERCICIOS:
        raise Http404("Ejercicio no encontrado")
    return EJERCICIOS[ejercicio_id]


# --- Intentos de la partida actual (en la sesión) ---------------------------

def _clave_sesion(clave):
    return f"parabolica:{clave}"


def _estado(request, clave):
    return request.session.get(_clave_sesion(clave), {"usados": 0, "terminado": False})


def _guardar_estado(request, clave, estado):
    request.session[_clave_sesion(clave)] = estado


def _reiniciar_estado(request, clave):
    request.session.pop(_clave_sesion(clave), None)
    servicios.reiniciar_pasos(request, clave)


# --- Vistas ------------------------------------------------------------------

@login_required
@ensure_csrf_cookie
def jugar(request, ejercicio_id):
    ejercicio = _ejercicio(ejercicio_id)
    clave = f"{APP}:{ejercicio_id}"
    _reiniciar_estado(request, clave)  # siempre se empieza desde cero
    materia = materia_de_reto(APP, ejercicio_id)
    return render(request, f"{APP}/reto.html", {
        "nombre_reto": "Tiro parabólico",
        "ejercicio": ejercicio,
        "datos_publicos": datos_publicos(ejercicio, ejercicio["intentos"]),
        "disparo_url": reverse(f"{APP}:disparo", args=[ejercicio_id]),
        "reintentar_url": reverse(f"{APP}:reintentar", args=[ejercicio_id]),
        "volver_url": reverse("mapa:materia", args=[materia["slug"]]) if materia else reverse("mapa:inicio"),
        "ya_resuelto": servicios.reto_resuelto(request.user, clave),
    })


@login_required
@require_POST
def disparo(request, ejercicio_id):
    """Recibe {"angulo":.., "fuerza":..}. Un rango inválido no consume
    intento (FA de validación). Respuesta cuando el rango es válido:
    { acerto, intentos_restantes, agotado, a, b, alcance, vertice, raices,
      completado, bitcoins_otorgados, bitcoins_total, ya_otorgado,
      mensaje }."""
    ejercicio = _ejercicio(ejercicio_id)
    clave = f"{APP}:{ejercicio_id}"
    try:
        datos = json.loads(request.body or "{}")
        angulo = float(datos.get("angulo"))
        fuerza = float(datos.get("fuerza"))
    except (json.JSONDecodeError, TypeError, ValueError):
        return JsonResponse({"error": "Datos inválidos"}, status=400)

    if not validar_rango(ejercicio, angulo, fuerza):
        return JsonResponse({"error": "Ángulo o fuerza fuera de rango"}, status=400)

    estado = _estado(request, clave)
    if estado["terminado"] or estado["usados"] >= ejercicio["intentos"]:
        return JsonResponse({"error": "No quedan intentos. Presiona Reintentar."}, status=400)

    trayectoria = calcular_disparo(ejercicio, angulo, fuerza)
    estado["usados"] += 1
    restantes = ejercicio["intentos"] - estado["usados"]
    estado["terminado"] = trayectoria["acerto"] or restantes == 0
    _guardar_estado(request, clave, estado)

    resultado = dict(trayectoria)
    resultado["intentos_restantes"] = restantes
    resultado["agotado"] = not trayectoria["acerto"] and restantes == 0

    if trayectoria["acerto"]:
        extra = servicios.procesar_paso(request, clave, 0, True, 1, ejercicio["bitcoins"])
        resultado.update(extra)
        resultado["ya_otorgado"] = resultado["bitcoins_otorgados"] == 0
        resultado["mensaje"] = "¡Impacto!"
    elif restantes == 0:
        resultado["mensaje"] = "Se agotaron los intentos. No obtuviste bitcoins."
    else:
        resultado["mensaje"] = f"No impactaste el blanco. Te quedan {restantes} intento(s)."
    return JsonResponse(resultado)


@login_required
@require_POST
def reintentar(request, ejercicio_id):
    """Botón «Reintentar»: restablece los 3 intentos, misma configuración
    del objetivo."""
    ejercicio = _ejercicio(ejercicio_id)
    _reiniciar_estado(request, f"{APP}:{ejercicio_id}")
    return JsonResponse({"intentos_restantes": ejercicio["intentos"]})
