"""
Color de acento por materia (no por reto individual): todos los retos de
una materia comparten un mismo color, igual en su tarjeta de la selección
(mapa/materia.html), en su propia pantalla de juego
(comun/context_processors.py la agrega como "color_acento" según la
materia a la que pertenece el reto) y en el mapa del campus
(mapa/views.py se lo pasa a cada edificio para la selección y los
marcadores sobre el mapa).

Por ahora todas las materias comparten el mismo rojo (el de siempre en el
mapa) para que mapa, selección y retos se vean como una sola interfaz.
La asignación por materia se deja tal cual para poder darle a una materia
su propio color el día que se necesite: basta con cambiar su entrada en
ACENTOS_MATERIA, nada más se toca.
"""

ROJO = "#ff3b44"
AZUL = "#59c7ff"
PURPURA = "#7c5cc4"
AMARILLO = "#e8b93d"
VERDE = "#3fae6a"

ACENTO_POR_DEFECTO = ROJO

ACENTOS_MATERIA = {
    "logica": ROJO,      # Lógica y Algoritmos
    "introprog": ROJO,   # Introducción a la Programación
    "linux": ROJO,
    "calculo": ROJO,
    "algebra": ROJO,
}


def acento_de_materia(slug):
    return ACENTOS_MATERIA.get(slug, ACENTO_POR_DEFECTO)
