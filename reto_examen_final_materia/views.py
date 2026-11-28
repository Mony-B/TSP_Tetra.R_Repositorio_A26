"""
Examen final de materia (CU-12, antes CU-04). Revisa las respuestas en el
servidor: las respuestas correctas están en ejercicios.py y nunca se mandan
al navegador. "ejercicio_id" es siempre el slug de una materia (mapa.temas);
no hay otros exámenes aquí (la Batalla Final sigue en la app "batalla").
"""
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse

from comun.colores import acento_de_materia
from mapa.temas import obtener_materia
from progreso import servicios

from .ejercicios import EJERCICIOS

APP = "reto_examen_final_materia"


@login_required
def jugar(request, ejercicio_id):
    """CU-12: examen final de la materia. Disponible en cualquier momento,
    sin requerir haber completado los retos (precondición del CU)."""
    datos = EJERCICIOS.get(ejercicio_id)
    materia = obtener_materia(ejercicio_id)
    if not datos or not materia:
        raise Http404("Examen no encontrado")

    volver_url = reverse("mapa:materia", args=[materia["slug"]])
    contexto = {
        "materia": materia,
        "examen": datos,
        "color_acento": acento_de_materia(materia["slug"]),
        "volver_url": volver_url,
    }

    if request.method == "POST":
        # FA-1 (tiempo agotado) y FE-1 (abandono) nunca mandan este POST
        # (ver examen.js): solo llega aquí un intento real, completo.
        preguntas = datos["preguntas"]
        aciertos = sum(
            1 for i, p in enumerate(preguntas)
            if request.POST.get(f"pregunta_{i}", "").strip() == p["respuesta"]
        )
        aprobado = aciertos >= datos["aciertos_minimos"]
        otorgados = servicios.registrar_examen(
            request.user, ejercicio_id, aciertos, len(preguntas), aprobado, datos["bitcoins"]
        )
        contexto.update(aciertos=aciertos, total=len(preguntas), aprobado=aprobado, otorgados=otorgados)
        return render(request, f"{APP}/resultado.html", contexto)

    # Solo se mandan texto y opciones, sin la respuesta correcta.
    contexto["preguntas"] = [
        {"indice": i, "texto": p["texto"], "opciones": p["opciones"]}
        for i, p in enumerate(datos["preguntas"])
    ]
    return render(request, f"{APP}/reto.html", contexto)
