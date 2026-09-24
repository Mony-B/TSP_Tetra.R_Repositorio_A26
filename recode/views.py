from django.shortcuts import render, get_object_or_404
from .models import Ruta, Subtema, Reto, ResolverReto, Examen, ResolverExamen


def lista_temas(request):
    """Pantalla principal: muestra todas las Rutas (le llaman 'temas' en el mockup)."""
    rutas = Ruta.objects.all()
    return render(request, "recode/pantalla_temas.html", {"rutas": rutas})


def lista_subtemas(request, tema_id):
    """Muestra los Subtemas de una Ruta específica."""
    ruta = get_object_or_404(Ruta, pk=tema_id)
    subtemas = ruta.subtemas.all()
    return render(request, "recode/pantalla_subtemas.html", {"tema": ruta, "subtemas": subtemas})


def _calcular_estado_retos(alumno, subtema):
    """
    Devuelve la lista de retos del subtema, cada uno con su .estado agregado:
    'completado', 'actual' (el siguiente disponible) o 'bloqueado'.
    Regla (CU01): un reto solo se desbloquea si el anterior en el mismo
    subtema ya fue resuelto exitosamente.
    """
    retos = list(subtema.retos.order_by("orden"))
    resueltos_ids = set(
        ResolverReto.objects.filter(
            alumno=alumno, reto__in=retos, completado_exitosamente=True
        ).values_list("reto_id", flat=True)
    )

    ya_encontro_actual = False
    for reto in retos:
        if reto.id_reto in resueltos_ids:
            reto.estado = "completado"
        elif not ya_encontro_actual:
            reto.estado = "actual"
            ya_encontro_actual = True
        else:
            reto.estado = "bloqueado"
    return retos, (len(resueltos_ids) == len(retos) and len(retos) > 0)


def seleccion_retos(request, subtema_id):
    """
    Muestra los retos de un subtema (con su estado) y el examen del tema,
    que solo se desbloquea si ya se completaron todos los retos del subtema.
    """
    subtema = get_object_or_404(Subtema, pk=subtema_id)
    # TEMPORAL: aún no hay login. Usamos el primer alumno como prueba.
    # Cuando armen el login, cambiar esto por: alumno = request.user.alumno
    from .models import Alumno
    alumno = Alumno.objects.first()

    retos, todos_completos = _calcular_estado_retos(alumno, subtema)

    examen = Examen.objects.filter(ruta=subtema.ruta).first()
    if examen and ResolverExamen.objects.filter(alumno=alumno, examen=examen, aprobado=True).exists():
        estado_examen = "completado"
    elif examen and todos_completos:
        estado_examen = "actual"
    else:
        estado_examen = "bloqueado"

    contexto = {
        "tema": subtema.ruta,
        "subtema": subtema,
        "estado_examen": estado_examen,
    }
    # los templates esperan reto_01, reto_02, reto_03 como variables sueltas
    for i, reto in enumerate(retos, start=1):
        contexto[f"reto_{i:02d}"] = reto

    return render(request, "recode/pantalla_seleccion_retos.html", contexto)


def resolver_reto(request, reto_id):
    """Pantalla para intentar un reto (aún falta el template de esta vista)."""
    reto = get_object_or_404(Reto, pk=reto_id)
    return render(request, "recode/reto_detalle.html", {"reto": reto})


def contestar_examen(request, tema_id):
    """Pantalla del examen final de la ruta (aún falta el template)."""
    ruta = get_object_or_404(Ruta, pk=tema_id)
    examen = get_object_or_404(Examen, ruta=ruta)
    return render(request, "recode/examen.html", {"examen": examen})