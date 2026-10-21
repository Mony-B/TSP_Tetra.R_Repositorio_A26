from mapa.temas import MATERIAS
from progreso import servicios

from .preguntas import EXAMENES


def tiene_examen(slug):
    return slug in EXAMENES and slug != "final"


def final_disponible(alumno):
    """Para la batalla final solo se exige aprobar el examen de cada materia.
    Si alguna materia todavía no tiene examen, la batalla no se abre."""
    aprobados = servicios.examenes_aprobados(alumno)
    return all(tiene_examen(m["slug"]) and m["slug"] in aprobados for m in MATERIAS)
