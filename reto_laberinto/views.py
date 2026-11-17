"""
Laberinto de sombras (CU-14). El movimiento del personaje y el dibujo del
laberinto son enteramente del navegador; el servidor solo interviene cuando
el personaje toca una respuesta, para decidir si es correcta (nunca lo
sabe el navegador). Los aciertos de la partida actual se guardan en la
sesión mientras se juega; si el alumno sale, no se guarda nada.
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

from .ejercicios import EJERCICIOS, datos_publicos, revisar_respuesta, total_pasos

APP = "reto_laberinto"


def _ejercicio(ejercicio_id):
    if ejercicio_id not in EJERCICIOS:
        raise Http404("Ejercicio no encontrado")
    return EJERCICIOS[ejercicio_id]


@login_required
@ensure_csrf_cookie
def jugar(request, ejercicio_id):
    """Pregunta 1 de 3 y un laberinto sin explorar (siempre se empieza
    desde el primer sector)."""
    ejercicio = _ejercicio(ejercicio_id)
    clave = f"{APP}:{ejercicio_id}"
    servicios.reiniciar_pasos(request, clave)
    materia = materia_de_reto(APP, ejercicio_id)
    return render(request, f"{APP}/reto.html", {
        "nombre_reto": "Laberinto de sombras",
        "ejercicio": ejercicio,
        "datos_publicos": datos_publicos(ejercicio, 0),
        "revisar_url": reverse(f"{APP}:revisar", args=[ejercicio_id]),
        "volver_url": reverse("mapa:materia", args=[materia["slug"]]) if materia else reverse("mapa:inicio"),
        "ya_resuelto": servicios.reto_resuelto(request.user, clave),
    })


@login_required
@require_POST
def revisar(request, ejercicio_id):
    """Recibe {"respuesta": "..."} (la pared que tocó el personaje).

    Respuesta: { correcto, completado, mensaje, bitcoins_otorgados,
                 bitcoins_total, siguiente (solo si acertó y faltan
                 preguntas), ya_otorgado (solo al completar) }."""
    ejercicio = _ejercicio(ejercicio_id)
    clave = f"{APP}:{ejercicio_id}"
    try:
        datos = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    if not isinstance(datos, dict):
        return JsonResponse({"error": "JSON inválido"}, status=400)

    total = total_pasos(ejercicio)
    paso_actual = len(servicios.pasos_correctos(request, clave))
    if paso_actual >= total:
        return JsonResponse({"error": "El reto ya no tiene preguntas pendientes"}, status=400)

    correcto = revisar_respuesta(ejercicio, paso_actual, str(datos.get("respuesta", "")))
    resultado = servicios.procesar_paso(request, clave, paso_actual, correcto, total, ejercicio["bitcoins"])

    if correcto:
        resultado["mensaje"] = "Ruta correcta. Acceso concedido."
        if resultado["completado"]:
            resultado["ya_otorgado"] = resultado["bitcoins_otorgados"] == 0
        else:
            resultado["siguiente"] = datos_publicos(ejercicio, paso_actual + 1)
    else:
        resultado["mensaje"] = "Respuesta incorrecta. Vuelve a explorar."
    return JsonResponse(resultado)
