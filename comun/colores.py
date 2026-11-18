"""
Dos cosas distintas, cada una con su propio color:

1. Color de acento por app de reto (ACENTOS_RETO / acento_de): se usa en la
   tarjeta de cada reto en la selección (mapa/materia.html) y en la propia
   pantalla de juego del reto (comun/context_processors.py la agrega como
   "color_acento" según la app que se está jugando). No depende de la
   materia: dos retos de la misma materia pueden tener distinto color si
   son de apps distintas, y el mismo reto se ve igual sin importar en qué
   materia esté colocado.

2. Color del mapa del campus (ACENTO_MAPA / acento_de_materia): el
   marco/selección de cada edificio en el mapa (mapa/views.py, mapa.js).
   Por ahora es un solo rojo para los 5, para que el mapa se vea como una
   sola interfaz; se deja la función por si se necesita diferenciarlos más
   adelante.
"""

TEAL = "#2f9c8f"
PURPURA = "#7c5cc4"
NARANJA = "#c98a2e"
AZUL = "#59c7ff"
ROJO = "#ff3b44"
MAGENTA = "#ff2fb0"  # red corrupta (CU03): no es un reto de materia, color propio

ACENTO_POR_DEFECTO = AZUL

ACENTOS_RETO = {
    "reto_sopa_letras": TEAL,
    "reto_ordenamiento": TEAL,
    "reto_comandos_linux": TEAL,       # incluye la terminal: queda en verde/teal
    "reto_algebra_booleana": PURPURA,
    "reto_obtener_termino": PURPURA,
    "reto_conceptos": PURPURA,
    "reto_clasificar": NARANJA,
    "reto_parabolica": NARANJA,
    "reto_ecuaciones": AZUL,
    "reto_laberinto": AZUL,
    "red_corrupta": MAGENTA,
}


def acento_de(app):
    return ACENTOS_RETO.get(app, ACENTO_POR_DEFECTO)


# --- Mapa del campus: un solo rojo para las 5 materias ----------------------

ACENTO_MAPA = ROJO


def acento_de_materia(slug):
    return ACENTO_MAPA
