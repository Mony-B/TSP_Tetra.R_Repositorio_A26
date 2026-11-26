"""
Calcular trayectoria parabólica (CU-12): ajustar ángulo y fuerza para
impactar un blanco fijo, con 3 intentos.

La física es la misma que se validó en el prototipo (velocidad en función
de la fuerza, caída por gravedad), pero aquí se calcula en el servidor:
el navegador nunca decide si un disparo acierta, solo anima la trayectoria
con los coeficientes que el servidor calculó.
"""
import math

EJERCICIOS = {
    "cuadraticas": {
        "titulo": "Tiro parabólico",
        "bitcoins": 30,
        "intentos": 3,
        # Unidades didácticas arbitrarias (iguales a las del prototipo),
        # no metros reales: lo importante es la forma de la parábola.
        "gravedad": 700,
        "angulo_min": 10,
        "angulo_max": 80,
        "fuerza_min": 20,
        "fuerza_max": 100,
        "objetivo_x": 560,
        "objetivo_y": 18,
        "objetivo_radio": 20,
    },
}


def datos_publicos(ejercicio, intentos_restantes):
    """Lo que ve el navegador: rangos de los controles, posición del
    objetivo (R90) e intentos restantes. Nunca se manda si un ángulo o
    fuerza concretos acertarían."""
    return {
        "angulo_min": ejercicio["angulo_min"],
        "angulo_max": ejercicio["angulo_max"],
        "fuerza_min": ejercicio["fuerza_min"],
        "fuerza_max": ejercicio["fuerza_max"],
        "objetivo_x": ejercicio["objetivo_x"],
        "objetivo_y": ejercicio["objetivo_y"],
        "objetivo_radio": ejercicio["objetivo_radio"],
        "intentos": ejercicio["intentos"],
        "intentos_restantes": intentos_restantes,
    }


def validar_rango(ejercicio, angulo, fuerza):
    return (
        ejercicio["angulo_min"] <= angulo <= ejercicio["angulo_max"]
        and ejercicio["fuerza_min"] <= fuerza <= ejercicio["fuerza_max"]
    )


def calcular_disparo(ejercicio, angulo, fuerza):
    """Calcula la trayectoria (misma fórmula validada en el prototipo) y si
    impacta el blanco fijo del ejercicio.

    Devuelve un diccionario con los coeficientes de y(x) = b·x − a·x², el
    alcance, el vértice, las raíces y si acertó.
    """
    theta = math.radians(angulo)
    velocidad = 110 + fuerza * 6
    a = ejercicio["gravedad"] / (2 * velocidad**2 * math.cos(theta) ** 2)
    b = math.tan(theta)
    alcance = b / a if a else 0

    objetivo_x = ejercicio["objetivo_x"]
    objetivo_y = ejercicio["objetivo_y"]
    radio = ejercicio["objetivo_radio"]

    altura_en_objetivo = b * objetivo_x - a * objetivo_x**2
    acerto = objetivo_x <= alcance and abs(altura_en_objetivo - objetivo_y) <= radio

    vertice_x = b / (2 * a) if a else 0
    vertice_y = b * vertice_x - a * vertice_x**2

    return {
        "a": a,
        "b": b,
        "alcance": alcance,
        "vertice": {"x": vertice_x, "y": vertice_y},
        "raices": {"x1": 0, "x2": alcance},
        "acerto": acerto,
    }
