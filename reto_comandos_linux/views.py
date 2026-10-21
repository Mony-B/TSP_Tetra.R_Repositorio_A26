"""
Comandos de Linux (CU-06): obtener la contraseña en una terminal simulada.

Todo se interpreta y revisa en el servidor: el sistema de archivos y la
contraseña están en ejercicios.py y solo llegan al navegador como salida de
un comando. El estado de la partida (carpeta actual, archivos que el alumno
crea o mueve, usuario y permisos) se guarda en la sesión mientras se juega; si
el alumno sale o recarga, empieza desde cero (el reto solo tiene dos estados:
completado o no). Al abrir la puerta se registra con progreso, que da los
bitcoins solo la primera vez.
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

from .ejercicios import (
    EJERCICIOS,
    LIMITE_COMANDO,
    datos_publicos,
    ejecutar,
    estado_inicial,
    estado_valido,
    prompt,
    revisar_clave,
)

APP = "reto_comandos_linux"


def _ejercicio(ejercicio_id):
    """Devuelve el ejercicio o responde 404 si no existe."""
    if ejercicio_id not in EJERCICIOS:
        raise Http404("Ejercicio no encontrado")
    return EJERCICIOS[ejercicio_id]


def _json(request):
    """Lee el cuerpo JSON; devuelve None si no es un objeto válido."""
    try:
        datos = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return None
    return datos if isinstance(datos, dict) else None


# --- Estado de la partida (en la sesión) ------------------------------------------


def _clave_sesion(clave):
    """Nombre con el que se guarda la partida en la sesión."""
    return f"linux:{clave}"


def _estado(request, ejercicio, clave):
    """Devuelve la partida guardada o una nueva si no hay o no es válida."""
    estado = request.session.get(_clave_sesion(clave))
    return estado if estado_valido(ejercicio, estado) else estado_inicial(ejercicio)


def _reiniciar(request, clave):
    """Borra la partida de la sesión y los pasos del reto."""
    request.session.pop(_clave_sesion(clave), None)
    servicios.reiniciar_pasos(request, clave)


# --- Vistas -------------------------------------------------------------------------


@login_required
@ensure_csrf_cookie
def jugar(request, ejercicio_id):
    """Paso 1: terminal en el directorio inicial, la puerta y Salir / Rendirse."""
    ejercicio = _ejercicio(ejercicio_id)
    clave = f"{APP}:{ejercicio_id}"
    _reiniciar(request, clave)  # siempre se empieza desde cero
    materia = materia_de_reto(APP, ejercicio_id)
    return render(
        request,
        f"{APP}/reto.html",
        {
            "nombre_reto": "Comandos de Linux",
            "ejercicio": ejercicio,
            "datos_publicos": datos_publicos(ejercicio),
            "revisar_url": reverse(f"{APP}:revisar", args=[ejercicio_id]),
            "comando_url": reverse(f"{APP}:comando", args=[ejercicio_id]),
            "volver_url": (
                reverse("mapa:materia", args=[materia["slug"]])
                if materia
                else reverse("mapa:inicio")
            ),
            "ya_resuelto": servicios.reto_resuelto(request.user, clave),
        },
    )


@login_required
@require_POST
def comando(request, ejercicio_id):
    """Pasos 2-3 (FA-1, FA-2): recibe {"comando": "ls"} y contesta con
    { salida, error, limpiar, prompt, oculto }. Los errores del comando no son
    errores HTTP: son salida normal de la terminal. `oculto` es True cuando la
    siguiente línea es una contraseña (su) y no debe mostrarse."""
    ejercicio = _ejercicio(ejercicio_id)
    clave = f"{APP}:{ejercicio_id}"
    datos = _json(request)
    if datos is None:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    linea = str(datos.get("comando", ""))
    if len(linea) > LIMITE_COMANDO:
        return JsonResponse({"error": "Comando demasiado largo"}, status=400)

    estado = _estado(request, ejercicio, clave)
    resultado = ejecutar(ejercicio, estado, linea)
    request.session[_clave_sesion(clave)] = estado
    return JsonResponse({**resultado, "prompt": prompt(estado)})


@login_required
@require_POST
def revisar(request, ejercicio_id):
    """Pasos 5-8 (FA-3): recibe {"respuesta": "clave"}.

    Respuesta: { correcto, completado, mensaje, bitcoins_otorgados,
                 bitcoins_total, ya_otorgado (solo si correcto) }
    Con la clave incorrecta la puerta sigue cerrada y no hay límite de intentos.
    """
    ejercicio = _ejercicio(ejercicio_id)
    datos = _json(request)
    if datos is None:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    correcto = revisar_clave(ejercicio, str(datos.get("respuesta", "")))
    # progreso registra el reto y da los bitcoins solo la primera vez.
    resultado = servicios.procesar_paso(
        request,
        f"{APP}:{ejercicio_id}",
        0,
        correcto,
        1,
        ejercicio["bitcoins"],
    )
    if correcto:
        resultado["ya_otorgado"] = resultado["bitcoins_otorgados"] == 0
        resultado["mensaje"] = "¡La puerta se abrió!"
    else:
        resultado["mensaje"] = "Contraseña incorrecta. La puerta sigue cerrada."
    return JsonResponse(resultado)
