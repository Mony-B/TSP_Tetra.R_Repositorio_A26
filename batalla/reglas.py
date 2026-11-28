from mapa.temas import MATERIAS
from progreso import servicios
from reto_examen_final_materia.ejercicios import EJERCICIOS as EXAMENES_MATERIA


def tiene_examen(slug):
    return slug in EXAMENES_MATERIA


def final_disponible(alumno):
    """Para la batalla final solo se exige aprobar el examen de cada materia.
    Si alguna materia todavía no tiene examen, la batalla no se abre."""
    aprobados = servicios.examenes_aprobados(alumno)
    return all(tiene_examen(m["slug"]) and m["slug"] in aprobados for m in MATERIAS)
