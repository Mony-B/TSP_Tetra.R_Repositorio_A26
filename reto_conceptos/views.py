"""
Relacionar conceptos (CU-13). Los carretes se giran en el navegador, sin
llamar al servidor; solo al intentar una combinación se manda al servidor,
que es quien decide si es válida y no estaba resuelta en la ronda. El
progreso de la ronda en curso se guarda en la sesión; si el alumno sale, no
se guarda (empieza de cero la próxima vez).
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

from .ejercicios import EJERCICIOS, datos_publicos, total_rondas, verificar_combinacion

APP = "reto_conceptos"


def _ejercicio(ejercicio_id):
    if ejercicio_id not in EJERCICIOS:
        raise Http404("Ejercicio no encontrado")
    return EJERCICIOS[ejercicio_id]


# --- Progreso de la partida actual (en la sesión) ---------------------------

def _clave_sesion(clave):
    return f"conceptos:{clave}"


def _estado(request, clave):
    return request.session.get(_clave_sesion(clave), {"ronda": 0, "resueltas": []})


def _guardar_estado(request, clave, estado):
    request.session[_clave_sesion(clave)] = estado


def _reiniciar_estado(request, clave):
    request.session.pop(_clave_sesion(clave), None)
    servicios.reiniciar_pasos(request, clave)


@login_required
@ensure_csrf_cookie
def jugar(request, ejercicio_id):
    ejercicio = _ejercicio(ejercicio_id)
    clave = f"{APP}:{ejercicio_id}"
    _reiniciar_estado(request, clave)  # siempre se empieza desde cero
    materia = materia_de_reto(APP, ejercicio_id)
    return render(request, f"{APP}/reto.html", {
        "nombre_reto": "Relacionar conceptos",
        "ejercicio": ejercicio,
        "datos_publicos": datos_publicos(ejercicio),
        "revisar_url": reverse(f"{APP}:verificar", args=[ejercicio_id]),
        "volver_url": reverse("mapa:materia", args=[materia["slug"]]) if materia else reverse("mapa:inicio"),
        "ya_resuelto": servicios.reto_resuelto(request.user, clave),
    })


@login_required
@require_POST
def verificar(request, ejercicio_id):
    """Recibe {"concepto":.., "palabra":.., "definicion":..} (los textos que
    quedaron alineados). Respuesta:
      { correcto, ya_resuelta, resueltas, total, ronda, ultima_ronda,
        completado, bitcoins_otorgados, bitcoins_total, ya_otorgado }."""
    ejercicio = _ejercicio(ejercicio_id)
    clave = f"{APP}:{ejercicio_id}"
    try:
        datos = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    if not isinstance(datos, dict):
        return JsonResponse({"error": "JSON inválido"}, status=400)

    concepto = str(datos.get("concepto", ""))
    palabra = str(datos.get("palabra", ""))
    definicion = str(datos.get("definicion", ""))

    estado = _estado(request, clave)
    ronda = estado["ronda"]
    total = len(ejercicio["rondas"][ronda])

    if not verificar_combinacion(ejercicio, ronda, concepto, palabra, definicion):
        return JsonResponse({"correcto": False, "ronda": ronda, "resueltas": len(estado["resueltas"]), "total": total})

    clave_combo = f"{concepto}|{palabra}|{definicion}"
    if clave_combo in estado["resueltas"]:
        return JsonResponse({
            "correcto": False, "ya_resuelta": True,
            "ronda": ronda, "resueltas": len(estado["resueltas"]), "total": total,
        })

    estado["resueltas"].append(clave_combo)
    completada_ronda = len(estado["resueltas"]) >= total
    ultima_ronda = ronda >= total_rondas(ejercicio) - 1

    if completada_ronda and not ultima_ronda:
        estado["ronda"] = ronda + 1
        estado["resueltas"] = []
        _guardar_estado(request, clave, estado)
        return JsonResponse({
            "correcto": True, "resueltas": total, "total": total,
            "ronda": ronda, "siguiente_ronda": ronda + 1, "completado": False,
        })

    if completada_ronda and ultima_ronda:
        resultado = servicios.procesar_paso(request, clave, 0, True, 1, ejercicio["bitcoins"])
        resultado["ya_otorgado"] = resultado["bitcoins_otorgados"] == 0
        resultado.update({"correcto": True, "resueltas": total, "total": total, "ronda": ronda})
        _reiniciar_estado(request, clave)
        return JsonResponse(resultado)

    _guardar_estado(request, clave, estado)
    return JsonResponse({
        "correcto": True, "resueltas": len(estado["resueltas"]), "total": total,
        "ronda": ronda, "completado": False,
    })
