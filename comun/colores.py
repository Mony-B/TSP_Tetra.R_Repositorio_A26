"""
Color de acento por materia (no por reto individual): todos los retos de
una materia comparten un mismo color, igual en su tarjeta de la selección
(mapa/materia.html) y en su propia pantalla de juego
(comun/context_processors.py la agrega como "color_acento" según la
materia a la que pertenece el reto).
"""

TEAL = "#2f9c8f"
PURPURA = "#7c5cc4"
NARANJA = "#c98a2e"
AZUL = "#59c7ff"

ACENTO_POR_DEFECTO = AZUL

ACENTOS_MATERIA = {
    "logica": PURPURA,
    "introprog": AZUL,
    "linux": TEAL,       # incluye la terminal: queda en verde/teal
    "calculo": NARANJA,
    "algebra": AZUL,
}


def acento_de_materia(slug):
    return ACENTOS_MATERIA.get(slug, ACENTO_POR_DEFECTO)
