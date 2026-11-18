"""
Color de acento por reto (app de Django), igual que el prototipo integrado:
cada tipo de reto tiene su propio color en vez de un solo acento para todos.

Se usa en dos lugares con el mismo valor para que se vea como una sola
interfaz: la tarjeta de cada reto en mapa/materia.html (mapa/temas.py la
agrega a info_reto) y la pantalla del propio reto (comun/context_processors.py
la agrega como "color_acento" a partir del app_name de la URL).
"""

TEAL = "#2f9c8f"
PURPURA = "#7c5cc4"
NARANJA = "#c98a2e"
AZUL = "#59c7ff"

ACENTO_POR_DEFECTO = AZUL

ACENTOS = {
    "reto_sopa_letras": TEAL,
    "reto_ordenamiento": TEAL,
    "reto_comandos_linux": TEAL,       # la terminal, en verde/teal
    "reto_algebra_booleana": PURPURA,
    "reto_obtener_termino": PURPURA,
    "reto_conceptos": PURPURA,
    "reto_clasificar": NARANJA,
    "reto_parabolica": NARANJA,
    "reto_ecuaciones": AZUL,
    "reto_laberinto": AZUL,
}


def acento_de(app_name):
    return ACENTOS.get(app_name, ACENTO_POR_DEFECTO)
