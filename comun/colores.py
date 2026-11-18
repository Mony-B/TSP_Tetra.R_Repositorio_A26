"""
Color de acento por materia (no por reto individual): todos los retos de
una materia comparten un mismo color, igual en su tarjeta de la selección
(mapa/materia.html) y en su propia pantalla de juego
(comun/context_processors.py la agrega como "color_acento" según la
materia a la que pertenece el reto), y también en el mapa del campus
(mapa/views.py se lo pasa a cada edificio para la selección y los
marcadores sobre el mapa).
"""

AZUL = "#59c7ff"
PURPURA = "#7c5cc4"
AMARILLO = "#e8b93d"
VERDE = "#3fae6a"
ROJO = "#e2434c"

ACENTO_POR_DEFECTO = AZUL

ACENTOS_MATERIA = {
    "logica": ROJO,        # Lógica y Algoritmos
    "introprog": PURPURA,  # Introducción a la Programación
    "linux": AZUL,
    "calculo": AMARILLO,
    "algebra": VERDE,
}


def acento_de_materia(slug):
    return ACENTOS_MATERIA.get(slug, ACENTO_POR_DEFECTO)
