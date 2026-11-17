"""
Resolver reto de ordenamiento (CU-11).

Colocar y retirar pasos de la línea de secuencia ocurre solo en el navegador
(nada que guardar hasta que el alumno presiona "Verificar"). El servidor
nunca recibe ni expone el orden correcto; solo valida la secuencia completa
que el alumno arma y, si es correcta, registra el reto con progreso.
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

from .ejercicios import EJERCICIOS, datos_publicos, verificar_secuencia

APP = "reto_ordenamiento"


def _ejercicio(ejercicio_id):
    if ejercicio_id not in EJERCICIOS:
        raise Http404("Ejercicio no encontrado")
    return EJERCICIOS[ejercicio_id]


@login_required
@ensure_csrf_cookie
def jugar(request, ejercicio_id):
    """Misión, pasos desordenados y línea de secuencia vacía (R83)."""
    ejercicio = _ejercicio(ejercicio_id)
    clave = f"{APP}:{ejercicio_id}"
    materia = materia_de_reto(APP, ejercicio_id)
    return render(request, f"{APP}/reto.html", {
        "nombre_reto": "Ordenar pasos",
        "ejercicio": ejercicio,
        "datos_publicos": datos_publicos(ejercicio),
        "revisar_url": reverse(f"{APP}:verificar", args=[ejercicio_id]),
        "volver_url": reverse("mapa:materia", args=[materia["slug"]]) if materia else reverse("mapa:inicio"),
        "ya_resuelto": servicios.reto_resuelto(request.user, clave),
    })


@login_required
@require_POST
def verificar(request, ejercicio_id):
    """Recibe {"secuencia": [id_paso|null, ...]} (R85).

    Respuesta:
      - vacíos (FA-2): { "vacios": [posiciones] }
      - orden incorrecto (FA-1): { "correcto": false }
      - éxito: { "correcto": true, "completado": true, "bitcoins_otorgados",
        "bitcoins_total" }
    """
    ejercicio = _ejercicio(ejercicio_id)
    try:
        datos = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    secuencia = datos.get("secuencia")
    if not isinstance(secuencia, list):
        return JsonResponse({"error": "Secuencia inválida"}, status=400)

    vacios, correcta = verificar_secuencia(ejercicio, secuencia)
    if vacios:
        return JsonResponse({"correcto": False, "vacios": vacios})
    if not correcta:
        return JsonResponse({"correcto": False})

    clave = f"{APP}:{ejercicio_id}"
    resultado = servicios.procesar_paso(request, clave, 0, True, 1, ejercicio["bitcoins"])
    resultado["ya_otorgado"] = resultado["bitcoins_otorgados"] == 0
    return JsonResponse(resultado)
