from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import finders
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.decorators.csrf import ensure_csrf_cookie

from mapa.temas import obtener_materia
from progreso import servicios


@login_required
@ensure_csrf_cookie
def ver(request, slug):
    """Entrega la página de la novela (Monogatari) de una materia."""
    materia = obtener_materia(slug)
    if not materia:
        raise Http404("Materia no encontrada")
    historia = f"novela/historias/{slug}.js"
    if not finders.find(historia):
        historia = "novela/historias/generica.js"
    return render(request, "novela/novela.html", {"materia": materia, "historia": historia})


@login_required
def saltar(request, slug):
    if obtener_materia(slug):
        servicios.marcar_novela_vista(request.user, slug)
    return redirect("mapa:materia", slug=slug)
