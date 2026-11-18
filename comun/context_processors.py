from .colores import acento_de


def color_reto(request):
    """Pone "color_acento" en todas las pantallas de reto, según la app que
    se está jugando: app_name de la URL (cada reto_xxx/urls.py ya define
    app_name = "reto_xxx"), sin necesidad de que cada vista mande su propio
    color. Así reto_base.html usa el mismo mecanismo para todos los retos.
    """
    match = getattr(request, "resolver_match", None)
    app_name = getattr(match, "app_name", None) if match else None
    return {"color_acento": acento_de(app_name)}
