from .colores import ACENTO_POR_DEFECTO, ACENTO_RED_CORRUPTA


def color_reto(request):
    """Pone "color_acento" en todas las pantallas de reto, según la MATERIA
    a la que pertenece el reto que se está jugando (no según su app): el
    mismo reto (p. ej. reto_laberinto) puede verse de un color si está en
    Linux y de otro si está en Programación. Resuelve la materia con
    app_name y ejercicio_id, los dos ya presentes en la URL de cada reto
    (cada reto_xxx/urls.py define app_name = "reto_xxx" y recibe
    ejercicio_id), así reto_base.html usa el mismo mecanismo para todos los
    retos sin que cada vista mande su propio color.

    La red corrupta (CU03) no es un reto de materia -su app_name es
    "red_corrupta" y no manda ejercicio_id- así que se reconoce aparte y
    usa su propio acento fijo (magenta) en vez de cualquier materia.
    """
    # Import adentro de la función para evitar un ciclo de imports con mapa.
    from mapa.temas import materia_de_reto

    match = getattr(request, "resolver_match", None)
    app_name = getattr(match, "app_name", None) if match else None

    if app_name == "red_corrupta":
        return {"color_acento": ACENTO_RED_CORRUPTA}

    ejercicio_id = match.kwargs.get("ejercicio_id") if match else None
    materia = materia_de_reto(app_name, ejercicio_id) if app_name and ejercicio_id else None
    color_acento = materia["acento_retos"] if materia else ACENTO_POR_DEFECTO
    return {"color_acento": color_acento}
