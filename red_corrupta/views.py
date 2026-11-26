"""
Red corrupta (CU03): catálogo de pistas, navegable desde cualquier parte
(un reto activo o la navegación general), independiente de cualquier
materia o subtema. Ver red_corrupta/pistas.py para el catálogo y
progreso/servicios.py para lo que se guarda de cada alumno.

Snake (el minijuego de hackeo) es enteramente del navegador -no hay nada
que "revisar" en el servidor como en los demás retos: no es una pregunta
con respuesta correcta, es un juego de habilidad- así que el servidor
solo recibe el aviso de victoria y entrega la pista, igual que confía en
el navegador para todo el movimiento dentro del laberinto de sombras.
"""
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from comun.colores import acento_de_materia
from progreso import servicios

from .pistas import CATALOGO, PISTAS


def _origen_seguro(request):
    """El origen llega como querystring (?origen=/retos/.../); se valida
    para no construir un botón que mande a un sitio externo (open
    redirect). Si no es una URL interna válida, cae a la navegación
    general (mapa)."""
    origen = request.GET.get("origen", "")
    if origen and url_has_allowed_host_and_scheme(
        origen, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return origen
    return reverse("mapa:inicio")


@login_required
@ensure_csrf_cookie
def catalogo(request):
    """Flujo normal, paso 1: el catálogo completo, marcando qué pistas ya
    tiene el alumno (FA-4/R100: esas se ven con su definición de una vez,
    sin volver a cobrarlas)."""
    origen_url = _origen_seguro(request)
    origen_label = request.GET.get("origen_label") or ("Volver al reto" if request.GET.get("origen") else "Volver al mapa")
    obtenidas = servicios.pistas_obtenidas(request.user)

    materias = []
    for materia_slug, materia in CATALOGO.items():
        subtemas = []
        total_materia = 0
        obtenidas_materia = 0
        for subtema_slug, subtema in materia["subtemas"].items():
            pistas = []
            for p in subtema["pistas"]:
                pid = f"{materia_slug}:{subtema_slug}:{p['slug']}"
                ya_obtenida = pid in obtenidas
                total_materia += 1
                obtenidas_materia += 1 if ya_obtenida else 0
                pistas.append({
                    "id": pid,
                    "termino": p["termino"],
                    "obtenida": ya_obtenida,
                    "definicion": p["definicion"] if ya_obtenida else "",
                })
            subtemas.append({"nombre": subtema["nombre"], "pistas": pistas})
        materias.append({
            "slug": materia_slug,
            "nombre": materia["nombre"],
            "subtemas": subtemas,
            "acento": acento_de_materia(materia_slug),
            "total": total_materia,
            "obtenidas": obtenidas_materia,
        })

    return render(request, "red_corrupta/catalogo.html", {
        "materias": materias,
        "origen_url": origen_url,
        "origen_label": origen_label,
        "costo_pista": servicios.COSTO_PISTA,
    })


@login_required
@require_POST
def comprar(request, pista_id):
    """Flujo normal, pasos 3-5 / FA-1 (saldo insuficiente): compra directa
    con bitcoins. Nunca descuenta si el saldo no alcanza (R35); la
    confirmación de costo ya la pidió el navegador antes de llamar aquí
    (requisito especial 2)."""
    if pista_id not in PISTAS:
        raise Http404("Pista no encontrada")
    ok = servicios.comprar_pista(request.user, pista_id)
    bitcoins_total = servicios.obtener_progreso(request.user).bitcoins
    if not ok:
        return JsonResponse({"ok": False, "bitcoins_total": bitcoins_total})
    pista = PISTAS[pista_id]
    return JsonResponse({
        "ok": True,
        "bitcoins_total": bitcoins_total,
        "termino": pista["termino"],
        "definicion": pista["definicion"],
    })


@login_required
@require_POST
def snake_completado(request, pista_id):
    """FA-1 (4a.4): victoria en Snake. El navegador decide cuándo se gana
    (mecánica de habilidad, no una respuesta que calificar); aquí solo se
    entrega la pista sin tocar el saldo."""
    if pista_id not in PISTAS:
        raise Http404("Pista no encontrada")
    servicios.otorgar_pista_snake(request.user, pista_id)
    bitcoins_total = servicios.obtener_progreso(request.user).bitcoins
    pista = PISTAS[pista_id]
    return JsonResponse({
        "ok": True,
        "bitcoins_total": bitcoins_total,
        "termino": pista["termino"],
        "definicion": pista["definicion"],
    })
