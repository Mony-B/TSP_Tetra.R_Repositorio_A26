import json
import random
import time

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from batalla.reglas import final_disponible
from comun.colores import ROJO
from progreso import servicios

from . import ejercicios

APP = "batalla_final"
RETO_CLAVE = "batalla_final:kernel"  # "Re:Code completado" (sin bitcoins)
SESION = "batalla_final"


def _estado(request):
    """Estado de la batalla en curso (vive en la sesión, no en la base)."""
    return request.session.get(SESION)


def _guardar(request, estado):
    request.session[SESION] = estado
    request.session.modified = True


def _error(mensaje, status=400):
    return JsonResponse({"error": mensaje}, status=status)


def _datos(request):
    """Cuerpo JSON de la petición; {} si viene vacío o mal formado."""
    try:
        datos = json.loads(request.body or "{}")
    except ValueError:
        return {}
    return datos if isinstance(datos, dict) else {}


def _limite(estado):
    """Segundos permitidos para el reto actual (fijos por tipo, R78b)."""
    return ejercicios.TIEMPO[ejercicios.RETOS[estado["actual"]]["tipo"]]


def _transcurrido(estado):
    """Segundos que lleva el reto actual sin contar el tiempo en pausa."""
    ahora = estado["pausa_inicio"] or time.time()
    return ahora - estado["inicio"] - estado["pausado_total"]


def _presentar_reto(estado):
    """Elige el siguiente reto de la cola mezclada y arranca su reloj (R78).

    Cuando la cola se agota se vuelve a armar: los retos pueden repetirse con
    la misma dificultad y el mismo tiempo por tipo.
    """
    if not estado["cola"]:
        cola = list(range(len(ejercicios.RETOS)))
        random.shuffle(cola)
        if len(cola) > 1 and cola[0] == estado["ultimo"]:
            cola.append(cola.pop(0))
        estado["cola"] = cola
    indice = estado["cola"].pop(0)
    estado.update(
        actual=indice,
        ultimo=indice,
        ronda=estado["ronda"] + 1,
        inicio=time.time(),
        pausa_inicio=None,
        pausado_total=0.0,
    )
    return ejercicios.datos_publicos(indice)


def _resolver(request, estado, correcto, motivo=""):
    """Aplica daño o cura, cierra el reto actual y arma la respuesta JSON.

    Respuesta: {correcto, motivo, vida, delta, victoria}
    """
    if correcto:
        delta = -min(ejercicios.DANO, estado["vida"])
    else:
        delta = min(ejercicios.CURA, ejercicios.VIDA_INICIAL - estado["vida"])
    estado["vida"] += delta
    estado["actual"] = None
    victoria = estado["vida"] <= 0
    if victoria:
        # Re:Code completado, una sola vez y sin bitcoins (R81).
        servicios.registrar_reto(request.user, RETO_CLAVE, 0)
        request.session.pop(SESION, None)
    else:
        _guardar(request, estado)
    return JsonResponse(
        {
            "correcto": correcto,
            "motivo": motivo,
            "vida": estado["vida"],
            "delta": delta,
            "victoria": victoria,
        }
    )


@login_required
def jugar(request):
    """Pantalla de la batalla final. Solo se abre con todos los exámenes
    aprobados (R43); si no, se regresa al menú principal."""
    if not final_disponible(request.user):
        return redirect("mapa:inicio")
    contexto = {
        "color_acento": ROJO,
        "nombre_alumno": request.user.get_full_name() or request.user.username,
        "vida_inicial": ejercicios.VIDA_INICIAL,
        "dano": ejercicios.DANO,
        "cura": ejercicios.CURA,
    }
    return render(request, "batalla_final/batalla.html", contexto)


@login_required
@require_POST
def iniciar(request):
    """Empieza (o reinicia) la batalla con el Kernel al 100 %.

    No recibe datos. Respuesta: {vida, ronda, reto}, donde `reto` es lo que
    devuelve ejercicios.datos_publicos (sin la respuesta correcta).
    """
    if not final_disponible(request.user):
        return _error("La batalla final todavía no está disponible.", 403)
    estado = {
        "vida": ejercicios.VIDA_INICIAL,
        "ronda": 0,
        "cola": [],
        "ultimo": None,
        "actual": None,
        "inicio": 0.0,
        "pausa_inicio": None,
        "pausado_total": 0.0,
    }
    reto = _presentar_reto(estado)
    _guardar(request, estado)
    return JsonResponse(
        {"vida": estado["vida"], "ronda": estado["ronda"], "reto": reto}
    )


@login_required
@require_POST
def siguiente(request):
    """Presenta el siguiente reto (el reloj arranca aquí, R78b).

    No recibe datos. Respuesta: {ronda, reto}.
    """
    estado = _estado(request)
    if not estado or estado["actual"] is not None:
        return _error("No hay un reto pendiente por presentar.")
    reto = _presentar_reto(estado)
    _guardar(request, estado)
    return JsonResponse({"ronda": estado["ronda"], "reto": reto})


@login_required
@require_POST
def responder(request):
    """Revisa la respuesta del reto actual.

    Recibe: {"respuesta": <según el tipo>}
      opcion -> índice; orden -> lista de pasos; terminal -> texto;
      clasificar -> {elemento: índice de categoría}.
    Respuesta: {correcto, motivo, vida, delta, victoria}. Si llega fuera de
    tiempo, cuenta como fallo.
    """
    estado = _estado(request)
    if not estado or estado["actual"] is None:
        return _error("No hay un reto en curso.")
    if _transcurrido(estado) > _limite(estado) + ejercicios.GRACIA_SEGUNDOS:
        return _resolver(request, estado, False, "Se agotó el tiempo")
    respuesta = _datos(request).get("respuesta")
    correcto = ejercicios.es_correcta(estado["actual"], respuesta)
    return _resolver(request, estado, correcto, "" if correcto else "Reto fallado")


@login_required
@require_POST
def tiempo_agotado(request):
    """El navegador avisa que se acabó el tiempo: cuenta como reto fallado.

    No recibe datos. Se rechaza si en el servidor todavía queda tiempo, para
    que no sirva como atajo. Respuesta igual a la de `responder`.
    """
    estado = _estado(request)
    if not estado or estado["actual"] is None:
        return _error("No hay un reto en curso.")
    if _transcurrido(estado) < _limite(estado) - ejercicios.GRACIA_SEGUNDOS:
        return _error("Todavía queda tiempo.")
    return _resolver(request, estado, False, "Se agotó el tiempo")


@login_required
@require_POST
def pausa(request):
    """Pausa o reanuda el reloj mientras está abierta la confirmación de
    abandono (R80).

    Recibe: {"pausar": true|false}. Respuesta: {"ok": true}.
    """
    estado = _estado(request)
    if not estado or estado["actual"] is None:
        return _error("No hay un reto en curso.")
    pausar = bool(_datos(request).get("pausar"))
    if pausar and estado["pausa_inicio"] is None:
        estado["pausa_inicio"] = time.time()
    elif not pausar and estado["pausa_inicio"] is not None:
        estado["pausado_total"] += time.time() - estado["pausa_inicio"]
        estado["pausa_inicio"] = None
    _guardar(request, estado)
    return JsonResponse({"ok": True})


@login_required
@require_POST
def abandonar(request):
    """El alumno confirmó que abandona: se descarta la batalla sin marcar
    Re:Code como completado (R80). No recibe datos. Respuesta: {"ok": true}."""
    request.session.pop(SESION, None)
    return JsonResponse({"ok": True})
