from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render

from mapa.temas import obtener_materia
from progreso import servicios

from .preguntas import EXAMENES
from .reglas import final_disponible


@login_required
def examen(request, slug):
    """Examen de una materia o batalla final (slug = "final").
    Las respuestas se califican aquí, nunca en el navegador."""
    datos = EXAMENES.get(slug)
    if not datos:
        raise Http404("Examen no encontrado")
    if slug == "final" and not final_disponible(request.user):
        return redirect("mapa:inicio")

    materia = obtener_materia(slug)
    contexto = {
        "slug": slug,
        "examen": datos,
        "materia": materia,
        "es_final": slug == "final",
    }

    if request.method == "POST":
        preguntas = datos["preguntas"]
        aciertos = sum(
            1 for i, p in enumerate(preguntas)
            if request.POST.get(f"pregunta_{i}", "").strip() == p["respuesta"]
        )
        aprobado = aciertos >= datos["aciertos_minimos"]
        otorgados = servicios.registrar_examen(
            request.user, slug, aciertos, len(preguntas), aprobado, datos["bitcoins"]
        )
        contexto.update(aciertos=aciertos, total=len(preguntas), aprobado=aprobado, otorgados=otorgados)
        return render(request, "batalla/resultado.html", contexto)

    # Solo se mandan texto y opciones, sin la respuesta correcta.
    contexto["preguntas"] = [
        {"indice": i, "texto": p["texto"], "opciones": p["opciones"]}
        for i, p in enumerate(datos["preguntas"])
    ]
    return render(request, "batalla/examen.html", contexto)
