from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django.templatetags.static import static
from django.urls import reverse

from batalla.reglas import final_disponible, tiene_examen
from progreso import servicios

from .edificios import EDIFICIOS, KERNEL
from .temas import MATERIAS, obtener_materia, info_reto, retos_de_materia


def _imagen(nombre):
    return static(f"mapa/img/{nombre}") if nombre else None


@login_required
def inicio(request):
    """Mapa del campus. Cada materia es un edificio; se elige en la barra
    lateral y la primera vez que entras a una ves su novela.

    Estado de cada edificio:
      restaurado  -> examen de la materia aprobado
      en_progreso -> ya vio la novela o resolvió algún reto
      corrupto    -> todavía no la empieza
    """
    alumno = request.user
    vistas = servicios.novelas_vistas(alumno)
    resueltos = servicios.retos_resueltos(alumno)
    # Se arma con examen_aprobado(), que ya existe en progreso/servicios.py
    aprobados = {m["slug"] for m in MATERIAS if servicios.examen_aprobado(alumno, m["slug"])}

    edificios = []
    for materia in MATERIAS:
        slug = materia["slug"]
        claves = [r["clave"] for r in retos_de_materia(materia)]
        hechos = sum(1 for c in claves if c in resueltos)

        if slug in aprobados:
            estado = "restaurado"
        elif slug in vistas or hechos:
            estado = "en_progreso"
        else:
            estado = "corrupto"

        if not tiene_examen(slug):
            examen = "Sin examen todavía"
        elif slug in aprobados:
            examen = "Examen superado"
        else:
            examen = "Examen pendiente"

        if slug in vistas:
            url = reverse("mapa:materia", args=[slug])
        else:
            url = reverse("novela:ver", args=[slug])

        visual = EDIFICIOS[slug]
        edificios.append({
            "slug": slug,
            "nombre": materia["nombre"],
            "codigo": visual["codigo"],
            "desc": visual["desc"],
            "x": visual["x"],
            "y": visual["y"],
            "imagen": _imagen(visual["imagen"]),
            "villano": visual["villano"],
            "aliado": visual.get("aliado"),
            "estado": estado,
            "examen": examen,
            "retos": f"{hechos}/{len(claves)} retos" if claves else "Sin retos todavía",
            "url": url,
        })
    edificios.sort(key=lambda e: e["codigo"])

    abierto = final_disponible(alumno)
    kernel = {
        **KERNEL,
        "imagen": _imagen(KERNEL["imagen"]),
        "abierto": abierto,
        "url": reverse("batalla:examen", args=["final"]) if abierto else None,
    }
    restaurados = sum(1 for e in edificios if e["estado"] == "restaurado")

    return render(request, "mapa/inicio.html", {
        "edificios": edificios,
        "kernel": kernel,
        "restaurados": restaurados,
        "total": len(edificios),
        "datos_mapa": {"edificios": edificios, "kernel": kernel},
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