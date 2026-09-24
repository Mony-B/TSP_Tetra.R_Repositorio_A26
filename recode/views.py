from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from .models import (
    Ruta, Subtema, Reto, ResolverReto, Alumno, Examen, ResolverExamen,
    RetoCF, RetoCifrado, RetoDD, RetoDecision,
)


def lista_temas(request):
    rutas = Ruta.objects.all()
    return render(request, 'recode/pantalla_temas.html', {'rutas': rutas})


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


def _obtener_subtipo(reto):
    """Devuelve (tipo_str, instancia_especifica) del reto, según su subclase real."""
    mapa = ["retocf", "retocifrado", "retodd", "retodecision"]
    for attr in mapa:
        try:
            return attr, getattr(reto, attr)
        except ObjectDoesNotExist:
            continue
    return None, None


def _validar_respuesta(tipo, especifico, respuesta):
    if tipo == "retocf":
        blanks_esperados = [b.strip().lower() for b in especifico.estructura_frase.get("blanks", [])]
        blanks_usuario = [r.strip().lower() for r in respuesta.split("|")]
        return blanks_usuario == blanks_esperados

    if tipo == "retocifrado":
        return respuesta.strip() == especifico.acertijo_logico.get("respuesta", "").strip()

    if tipo == "retodecision":
        return respuesta.strip() == especifico.opciones_botones.get("correcta", "").strip()

    if tipo == "retodd":
        # el front debe mandar el mismo orden que "solucion" en catalogo_dd, separado por comas
        solucion = especifico.catalogo_dd.get("solucion", [])
        return [r.strip() for r in respuesta.split(",")] == solucion

    return False


def resolver_reto(request, reto_id):
    """Pantalla para intentar un reto: valida la respuesta, otorga puntos,
    y decide si desbloquear el siguiente reto, el siguiente subtema, o
    mostrar la felicitación final de la ruta."""
    reto = get_object_or_404(Reto, pk=reto_id)
    tipo, especifico = _obtener_subtipo(reto)

    # TEMPORAL: aún no hay login. Cambiar cuando exista: alumno = request.user.alumno
    alumno = Alumno.objects.first()

    if request.method == "POST":
        respuesta = request.POST.get("respuesta", "")
        es_correcta = _validar_respuesta(tipo, especifico, respuesta)

        ResolverReto.objects.create(
            alumno=alumno, reto=reto, completado_exitosamente=es_correcta
        )

        if not es_correcta:
            contexto = {"reto": reto, "tipo": tipo, "especifico": especifico, "incorrecto": True}
            return render(request, "recode/reto_detalle.html", contexto)

        # Respuesta correcta: otorgar puntos
        progreso = alumno.progreso
        progreso.puntos_exp += reto.recompensa_exp
        progreso.save()

        # ¿Hay siguiente reto en el mismo subtema?
        siguiente_reto = Reto.objects.filter(
            subtema=reto.subtema, orden=reto.orden + 1
        ).first()
        if siguiente_reto:
            return redirect("resolver_reto", reto_id=siguiente_reto.id_reto)

        # No hay más retos en este subtema: ¿hay siguiente subtema en la ruta?
        siguiente_subtema = Subtema.objects.filter(
            ruta=reto.subtema.ruta, orden=reto.subtema.orden + 1
        ).first()
        if siguiente_subtema:
            return render(request, "recode/reto_completado.html", {
                "reto": reto,
                "subtema_actual": reto.subtema,
                "siguiente_subtema": siguiente_subtema,
                "fin_ruta": False,
            })

        # No hay más subtemas: se completó toda la ruta
        return render(request, "recode/reto_completado.html", {
            "reto": reto,
            "subtema_actual": reto.subtema,
            "ruta": reto.subtema.ruta,
            "fin_ruta": True,
        })

    # GET: mostrar el reto
    contexto = {"reto": reto, "tipo": tipo, "especifico": especifico}
    return render(request, "recode/reto_detalle.html", contexto)


def contestar_examen(request, tema_id):
    """Pantalla del examen final de la ruta (aún falta el template)."""
    ruta = get_object_or_404(Ruta, pk=tema_id)
    examen = get_object_or_404(Examen, ruta=ruta)
    return render(request, "recode/examen.html", {"examen": examen})