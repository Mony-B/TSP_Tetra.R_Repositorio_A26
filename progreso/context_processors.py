def progreso_alumno(request):
    """Pone los bitcoins del alumno en todas las pantallas (barra superior)."""
    if not request.user.is_authenticated:
        return {}
    from .servicios import obtener_progreso
    return {"progreso_alumno": obtener_progreso(request.user)}
