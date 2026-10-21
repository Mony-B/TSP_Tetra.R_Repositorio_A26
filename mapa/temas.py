"""
Materias, subtemas y qué retos van en cada uno.

Van fijos en el código (no en la base de datos) porque no cambian.
Cada reto se apunta como ("nombre_de_la_app", "id_del_ejercicio"); el
ejercicio en sí (preguntas, respuestas, bitcoins) vive en ejercicios.py
de su app.
"""
from importlib import import_module

from django.urls import reverse


MATERIAS = [
    {
        "slug": "logica",
        "nombre": "Lógica y Algoritmos",
        "subtemas": [
            {"nombre": "Algoritmos", "retos": [("reto_sopa_letras", "algoritmos")]},
            {"nombre": "Lógica proposicional", "retos": [("reto_algebra_booleana", "proposicional")]},
            {"nombre": "Conjuntos", "retos": [("reto_obtener_termino", "conjuntos")]},
        ],
    },
    {
        "slug": "introprog",
        "nombre": "Introducción a la Programación",
        "subtemas": [
            {"nombre": "Conceptos básicos", "retos": [
                ("reto_obtener_termino", "conceptos-basicos-1"),
                ("reto_obtener_termino", "conceptos-basicos-2"),
                ("reto_obtener_termino", "conceptos-basicos-3"),
            ]},
        ],
    },
    {
        "slug": "linux",
        "nombre": "Linux",
        "subtemas": [
            {"nombre": "Exploración del entorno", "retos": [("reto_comandos_linux", "basicos")]},
            {"nombre": "Creación y manipulación de archivos", "retos": [("reto_comandos_linux", "archivos")]},
            {"nombre": "Lectura y filtrado de información", "retos": [("reto_comandos_linux", "filtrado")]},
            {"nombre": "Búsqueda avanzada", "retos": [("reto_comandos_linux", "busqueda")]},
            {"nombre": "Permisos y propiedad", "retos": [("reto_comandos_linux", "permisos")]},
        ],
    },
    {
        "slug": "calculo",
        "nombre": "Cálculo",
        "subtemas": [],
    },
    {
        "slug": "algebra",
        "nombre": "Álgebra",
        "subtemas": [
            {"nombre": "Ecuaciones", "retos": [("reto_ecuaciones", "lineales")]},
            {"nombre": "Desigualdades", "retos": [("reto_desigualdades", "lineales")]},
        ],
    },
]


def obtener_materia(slug):
    for materia in MATERIAS:
        if materia["slug"] == slug:
            return materia
    return None


def info_reto(app, ejercicio_id):
    """Datos para mostrar un reto en el mapa: título, liga y su clave en progreso."""
    ejercicios = import_module(f"{app}.ejercicios").EJERCICIOS
    ejercicio = ejercicios[ejercicio_id]
    return {
        "clave": f"{app}:{ejercicio_id}",
        "titulo": ejercicio["titulo"],
        "bitcoins": ejercicio["bitcoins"],
        "url": reverse(f"{app}:jugar", args=[ejercicio_id]),
    }


def retos_de_materia(materia):
    return [info_reto(app, ej) for sub in materia["subtemas"] for app, ej in sub["retos"]]


def materia_de_reto(app, ejercicio_id):
    """Para el botón de regresar de cada reto."""
    for materia in MATERIAS:
        for sub in materia["subtemas"]:
            if (app, ejercicio_id) in sub["retos"]:
                return materia
    return None