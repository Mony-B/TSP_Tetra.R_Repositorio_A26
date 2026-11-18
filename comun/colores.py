"""
Color de acento de cada materia (Álgebra, Cálculo, Lógica y Algoritmos,
Introducción a la Programación, Linux). Un solo valor por materia, no por
app de reto: dos retos de distinta app que estén en la misma materia se ven
del mismo color, y el mismo reto (misma app) se ve de un color si está en
una materia y de otro si está en otra (ver mapa/temas.py:materia_de_reto).

Se usa en dos lugares, que siempre comparten el mismo valor:
1. La tarjeta de cada reto en su pantalla de selección (mapa/materia.html).
2. La propia pantalla de juego del reto (comun/context_processors.py la
   agrega como "color_acento", resolviendo primero en qué materia está el
   reto que se está jugando).

El mapa del campus (el marco de cada edificio en mapa/views.py y mapa.js)
es independiente y usa su propio color fijo, ACENTO_MAPA, igual para las 5
materias, para que el mapa se vea como una sola interfaz.
"""

ROSA_CORAL = "#F184A8"
AZUL_ELECTRICO = "#72A7FF"
CIAN_TERMINAL = "#48C4D8"
VIOLETA_NEON = "#B18AF5"
NARANJA_AMBAR = "#F2A66B"
ROJO = "#ff3b44"

ACENTO_POR_DEFECTO = AZUL_ELECTRICO

ACENTOS_MATERIA = {
    "introprog": ROSA_CORAL,
    "algebra": AZUL_ELECTRICO,
    "linux": CIAN_TERMINAL,
    "logica": VIOLETA_NEON,
    "calculo": NARANJA_AMBAR,
}


def acento_de_materia(slug):
    return ACENTOS_MATERIA.get(slug, ACENTO_POR_DEFECTO)


# --- Mapa del campus: un solo rojo para las 5 materias ----------------------

ACENTO_MAPA = ROJO
