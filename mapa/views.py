from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse

from batalla.reglas import final_disponible, tiene_examen
from progreso import servicios

from .temas import MATERIAS, obtener_materia, info_reto


@login_required
def inicio(request):
    """Mapa de materias. La primera vez que entras a una, ves su novela."""
    vistas = servicios.novelas_vistas(request.user)
    materias = []
    for materia in MATERIAS:
        if materia["slug"] in vistas:
            url = reverse("mapa:materia", args=[materia["slug"]])
        else:
            url = reverse("novela:ver", args=[materia["slug"]])
        materias.append({**materia, "url": url})
    return render(request, "mapa/inicio.html", {
        "materias": materias,
        "final_disponible": final_disponible(request.user),
    })


@login_required
def materia(request, slug):
    """Subtemas de la materia con sus retos (todos disponibles) y el examen."""
    materia = obtener_materia(slug)
    if not materia:
        raise Http404("Materia no encontrada")

    resueltos = servicios.retos_resueltos(request.user)
    subtemas = []
    for sub in materia["subtemas"]:
        retos = [info_reto(app, ej) for app, ej in sub["retos"]]
        for reto in retos:
            reto["resuelto"] = reto["clave"] in resueltos
        subtemas.append({"nombre": sub["nombre"], "retos": retos})

    return render(request, "mapa/materia.html", {
        "materia": materia,
        "subtemas": subtemas,
        "tiene_examen": tiene_examen(slug),
        "examen_aprobado": servicios.examen_aprobado(request.user, slug),
    })
