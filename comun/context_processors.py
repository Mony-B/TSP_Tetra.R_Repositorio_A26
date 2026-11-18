from .colores import acento_de


def color_reto(request):
    """Pone "color_acento" en todas las pantallas, según la app del reto que
    se está jugando (request.resolver_match.app_name, que cada reto_xxx/urls.py
    ya define con app_name = "reto_xxx"). Así reto_base.html no necesita que
    cada vista mande su propio color: todas comparten el mismo mecanismo.
    """
    match = getattr(request, "resolver_match", None)
    app_name = getattr(match, "app_name", None) if match else None
    return {"color_acento": acento_de(app_name)}
