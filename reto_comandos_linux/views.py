"""
Comandos de Linux (CU-06). Revisa las respuestas en el servidor.
Las respuestas correctas están en ejercicios.py y nunca se mandan al navegador.
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

from .ejercicios import EJERCICIOS, datos_publicos, revisar_respuesta

APP = "reto_comandos_linux"


def _ejercicio(ejercicio_id):
    if ejercicio_id not in EJERCICIOS:
        raise Http404("Ejercicio no encontrado")
    return EJERCICIOS[ejercicio_id]


@login_required
@ensure_csrf_cookie
def jugar(request, ejercicio_id):
    ejercicio = _ejercicio(ejercicio_id)
    clave = f"{APP}:{ejercicio_id}"
    servicios.reiniciar_pasos(request, clave)
    materia = materia_de_reto(APP, ejercicio_id)
    return render(request, f"{APP}/reto.html", {
        "nombre_reto": "Comandos de Linux",
        "ejercicio": ejercicio,
        "datos_publicos": datos_publicos(ejercicio),
        "revisar_url": reverse(f"{APP}:revisar", args=[ejercicio_id]),
        "volver_url": reverse("mapa:materia", args=[materia["slug"]]) if materia else reverse("mapa:inicio"),
        "ya_resuelto": servicios.reto_resuelto(request.user, clave),
    })


@login_required
@require_POST
def revisar(request, ejercicio_id):
    """Recibe {"paso": n, "respuesta": "..."} y contesta si es correcta."""
    ejercicio = _ejercicio(ejercicio_id)
    try:
        datos = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    paso, correcto, mensaje = revisar_respuesta(ejercicio, datos.get("paso"), str(datos.get("respuesta", "")))
    if paso is None:
        return JsonResponse({"error": "Paso inválido"}, status=400)

    resultado = servicios.procesar_paso(
        request, f"{APP}:{ejercicio_id}", paso, correcto,
        ejercicio_total_pasos(ejercicio), ejercicio["bitcoins"],
    )
    resultado["mensaje"] = mensaje
    resultado["paso"] = paso
    return JsonResponse(resultado)


def ejercicio_total_pasos(ejercicio):
    return len(ejercicio["pasos"])
