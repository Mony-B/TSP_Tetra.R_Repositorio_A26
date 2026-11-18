from .colores import ACENTO_POR_DEFECTO


def color_reto(request):
    """Pone "color_acento" en todas las pantallas, según la materia de la que
    es el reto que se está jugando: misma app_name + ejercicio_id de la URL
    (cada reto_xxx/urls.py ya define app_name = "reto_xxx" y captura
    <slug:ejercicio_id>) para encontrar su materia con materia_de_reto() y
    tomar el color que ya trae esa materia (mapa/temas.py). Así reto_base.html
    no necesita que cada vista mande su propio color: todas comparten el
    mismo mecanismo.
    """
    match = getattr(request, "resolver_match", None)
    app_name = getattr(match, "app_name", None) if match else None
    ejercicio_id = match.kwargs.get("ejercicio_id") if match else None
    if not app_name or not ejercicio_id:
        return {"color_acento": ACENTO_POR_DEFECTO}

    from mapa.temas import materia_de_reto  # import tardío: evita ciclo con mapa

    materia = materia_de_reto(app_name, ejercicio_id)
    color = materia["acento"] if materia else ACENTO_POR_DEFECTO
    return {"color_acento": color}
