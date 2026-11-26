"""Vistas del reto de ecuaciones lineales (CU-07). Mismo patrón que reto_algebra_booleana:
jugar muestra el reto (siempre desde cero) y revisar valida en el servidor."""
import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from mapa.temas import materia_de_reto
from progreso import servicios

from . import ejercicios

APP = "reto_ecuaciones"


def _clave(ejercicio_id):
    return f"{APP}:{ejercicio_id}"


@login_required
@ensure_csrf_cookie   # la página necesita la cookie csrftoken para poder mandar el POST de /revisar/
def jugar(request, ejercicio_id):
    ejercicio = ejercicios.EJERCICIOS.get(ejercicio_id)
    if ejercicio is None:
        return redirect("mapa:inicio")
    servicios.reiniciar_pasos(request, _clave(ejercicio_id))      # salir y volver = empezar de cero
    materia = materia_de_reto(APP, ejercicio_id)
    return render(request, "reto_ecuaciones/reto.html", {
        "nombre_reto": "Ecuaciones lineales",
        "ejercicio": ejercicio,
        "datos_publicos": ejercicios.datos_publicos(ejercicio),
        "revisar_url": reverse("reto_ecuaciones:revisar", args=[ejercicio_id]),
        "volver_url": reverse("mapa:materia", args=[materia["slug"]]) if materia else reverse("mapa:inicio"),
        "ya_resuelto": servicios.reto_resuelto(request.user, _clave(ejercicio_id)),
    })
 
 
@login_required
@require_POST
def revisar(request, ejercicio_id):
    ejercicio = ejercicios.EJERCICIOS.get(ejercicio_id)
    if ejercicio is None:
        return JsonResponse({"error": "Reto no encontrado"}, status=404)
    try:
        datos = json.loads(request.body or b"{}")
    except ValueError:
        return JsonResponse({"error": "Petición inválida"}, status=400)
    paso, correcto, mensaje = ejercicios.revisar_respuesta(ejercicio, datos.get("paso"), str(datos.get("respuesta", "")))
    if paso is None:
        return JsonResponse({"error": "Paso inválido"}, status=400)
    resultado = servicios.procesar_paso(request, _clave(ejercicio_id), paso, correcto,
                                        len(ejercicio["pasos"]), ejercicio["bitcoins"])
    resultado.update({"mensaje": mensaje, "paso": paso})
    return JsonResponse(resultado)