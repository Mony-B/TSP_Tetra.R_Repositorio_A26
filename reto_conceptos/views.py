"""
Sopa de letras (CU-10). Revisa las respuestas en el servidor.
Django solo acepta una selección si forma uno de los conceptos de ejercicios.py.
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

APP = "reto_conceptos"


def _ejercicio(ejercicio_id):
    """Devuelve el ejercicio o responde 404 si no existe."""
    if ejercicio_id not in EJERCICIOS:
        raise Http404("Ejercicio no encontrado")
    return EJERCICIOS[ejercicio_id]


def _total_pasos(ejercicio):
    """Cuenta los conceptos que hay que encontrar para completar el reto."""
    return len(ejercicio["pasos"])


@login_required
@ensure_csrf_cookie
def jugar(request, ejercicio_id):
    """Muestra la sopa; cada vez que se abre, el reto empieza desde cero."""
    ejercicio = _ejercicio(ejercicio_id)
    clave = f"{APP}:{ejercicio_id}"
    servicios.reiniciar_pasos(request, clave)
    materia = materia_de_reto(APP, ejercicio_id)
    if materia:
        volver_url = reverse("mapa:materia", args=[materia["slug"]])
    else:
        volver_url = reverse("mapa:inicio")
    contexto = {
        "nombre_reto": "Sopa de letras",
        "ejercicio": ejercicio,
        "datos_publicos": datos_publicos(ejercicio),
        "revisar_url": reverse(f"{APP}:revisar", args=[ejercicio_id]),
        "volver_url": volver_url,
        "ya_resuelto": servicios.reto_resuelto(request.user, clave),
    }
    return render(request, f"{APP}/reto.html", contexto)


@login_required
@require_POST
def revisar(request, ejercicio_id):
    """Recibe {"respuesta": "..."} y contesta si la selección forma un concepto."""
    ejercicio = _ejercicio(ejercicio_id)
    try:
        datos = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    if not isinstance(datos, dict):
        return JsonResponse({"error": "JSON inválido"}, status=400)

    paso, correcto, mensaje = revisar_respuesta(
        ejercicio, str(datos.get("respuesta", ""))
    )
    resultado = servicios.procesar_paso(
        request,
        f"{APP}:{ejercicio_id}",
        paso,
        correcto,
        _total_pasos(ejercicio),
        ejercicio["bitcoins"],
    )
    resultado["mensaje"] = mensaje
    resultado["paso"] = paso
    return JsonResponse(resultado)
