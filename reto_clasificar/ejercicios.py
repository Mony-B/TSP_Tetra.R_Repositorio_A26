"""
Clasificar elementos por categorías (CU-08): contenido y reglas del reto.

El reto es reutilizable: cada entrada de EJERCICIOS define el enunciado, las
fichas, las categorías y la regla que decide a qué categoría pertenece cada
ficha. Para agregar un subtema solo se agrega una entrada nueva; la mecánica
(views.py y juego.js) no cambia.

En este conjunto los ejercicios son desigualdades en el plano: las fichas son
puntos (x, y) y las categorías son "Es solución" / "No es solución". La
categoría correcta NO se manda al navegador: se calcula aquí evaluando la
desigualdad con aritmética exacta (Fraction), sin errores de redondeo.
"""
import operator
from fractions import Fraction
from functools import cache

SI, NO = "si", "no"

CATEGORIAS = [
    {"id": SI, "nombre": "Es solución", "detalle": "(Verdadero)"},
    {"id": NO, "nombre": "No es solución", "detalle": "(Falso)"},
]

OPERADORES = {">": operator.gt, ">=": operator.ge, "<": operator.lt, "<=": operator.le}

RANGO = 6          # la gráfica va de -RANGO a RANGO en los dos ejes
CELDAS_POR_UNIDAD = 4


def _lineal(x):
    return 2 * x - 1


def _parabola(x):
    return x * x - 4


def _hiperbola(x):
    """2 / (x - 1); no está definida en x = 1."""
    return None if x == 1 else Fraction(2) / (x - 1)


def _recta(x):
    return x - 2


def _parabola_invertida(x):
    return 4 - x * x


# Cada desigualdad es "y <op> f(x)". Un punto es solución si cumple TODAS.
EJERCICIOS = {
    "lineales": {
        "nivel": 1,
        "subtema": "Desigualdades lineales",
        "titulo": "Desigualdades lineales",
        "instrucciones": "Arrastra cada punto a la caja correcta: ¿cumple la desigualdad?",
        "enunciado": ["y ≥ 2x − 1"],
        "desigualdades": [{"op": ">=", "f": _lineal}],
        "puntos": [(0, 0), (1, 1), (-2, -3), (2, 1), (3, 2), (-1, -4)],
        "ayuda": "Sustituye x e y en la desigualdad. Si la línea es sólida, el punto sobre ella también cuenta.",
        "bitcoins": 50,
    },
    "cuadraticas": {
        "nivel": 2,
        "subtema": "Desigualdades cuadráticas",
        "titulo": "Desigualdades cuadráticas",
        "instrucciones": "Arrastra cada punto a la caja correcta: ¿cumple la desigualdad?",
        "enunciado": ["y > x² − 4"],
        "desigualdades": [{"op": ">", "f": _parabola}],
        "puntos": [(0, 0), (3, 5), (1, -1), (2, -5), (0, -5), (-2, 4)],
        "ayuda": "Calcula x² − 4 con el valor de x. Con la línea punteada, el punto sobre la curva NO cuenta.",
        "bitcoins": 75,
    },
    "racionales": {
        "nivel": 3,
        "subtema": "Desigualdades racionales",
        "titulo": "Desigualdades racionales",
        "instrucciones": "Arrastra cada punto a la caja correcta: ¿cumple la desigualdad?",
        "enunciado": ["y ≤ 2 / (x − 1)"],
        "desigualdades": [{"op": "<=", "f": _hiperbola}],
        "puntos": [(2, 1), (3, 0), (0, -1), (0, -3), (2, 3), (4, 1)],
        "ayuda": "Calcula 2 / (x − 1) con el valor de x y compara con y. Cuidado con el signo cuando x < 1.",
        "bitcoins": 100,
    },
    "compuestas": {
        "nivel": 4,
        "subtema": "Desigualdades compuestas",
        "titulo": "Desigualdades compuestas",
        "instrucciones": "Un punto es solución solo si cumple las dos desigualdades a la vez.",
        "enunciado": ["y > x − 2", "y ≤ 4 − x²"],
        "desigualdades": [{"op": ">", "f": _recta}, {"op": "<=", "f": _parabola_invertida}],
        "puntos": [(0, 0), (1, 1), (-1, 3), (2, 0), (0, 5), (3, -1)],
        "ayuda": "Revisa cada desigualdad por separado; si falla una, el punto no es solución.",
        "bitcoins": 125,
    },
}


# --- Regla de clasificación (solo en el servidor) ---------------------------------

def es_solucion(ejercicio, x, y):
    for d in ejercicio["desigualdades"]:
        valor = d["f"](Fraction(x))
        if valor is None or not OPERADORES[d["op"]](Fraction(y), valor):
            return False
    return True


def categoria_correcta(ejercicio, ficha):
    return SI if es_solucion(ejercicio, ficha["x"], ficha["y"]) else NO


def fichas(ejercicio):
    """Fichas con id estable (f0, f1, ...) según su posición en la lista."""
    return [{"id": f"f{i}", "x": x, "y": y} for i, (x, y) in enumerate(ejercicio["puntos"])]


def evaluar_ficha(ejercicio, ficha_id, categoria):
    """Paso 5: ¿la ficha pertenece a la categoría elegida?

    Devuelve True / False, o None si la ficha o la categoría no existen.
    """
    if categoria not in (SI, NO):
        return None
    for ficha in fichas(ejercicio):
        if ficha["id"] == ficha_id:
            return categoria_correcta(ejercicio, ficha) == categoria
    return None


def verificar_completo(ejercicio, clasificadas):
    """Paso 6: ¿ya se clasificaron todas las fichas?"""
    return {f["id"] for f in fichas(ejercicio)} <= set(clasificadas)


# --- Lo que ve el navegador -------------------------------------------------------

def _curvas(ejercicio):
    """Polilíneas de cada frontera (se parten en las asíntotas o fuera de rango)."""
    curvas = []
    for d in ejercicio["desigualdades"]:
        tramos, tramo = [], []
        for k in range(-RANGO * 20, RANGO * 20 + 1):
            x = Fraction(k, 20)
            y = d["f"](x)
            if y is None or abs(y) > RANGO + 2:
                if len(tramo) > 1:
                    tramos.append(tramo)
                tramo = []
                continue
            tramo.append([float(x), round(float(y), 3)])
        if len(tramo) > 1:
            tramos.append(tramo)
        curvas.append({"solida": d["op"] in (">=", "<="), "tramos": tramos})
    return curvas


def _sombra(ejercicio):
    """Rejilla de la región solución: una cadena de '0'/'1' por fila (de arriba abajo)."""
    n = 2 * RANGO * CELDAS_POR_UNIDAD
    filas = []
    for j in range(n):
        y = RANGO - Fraction(2 * j + 1, 2 * CELDAS_POR_UNIDAD)
        fila = ""
        for i in range(n):
            x = -RANGO + Fraction(2 * i + 1, 2 * CELDAS_POR_UNIDAD)
            fila += "1" if es_solucion(ejercicio, x, y) else "0"
        filas.append(fila)
    return filas


@cache
def _grafica(ejercicio_id):
    ejercicio = EJERCICIOS[ejercicio_id]
    return {
        "rango": RANGO,
        "celdas": CELDAS_POR_UNIDAD,
        "curvas": _curvas(ejercicio),
        "sombra": _sombra(ejercicio),
    }


def datos_publicos(ejercicio_id):
    """Todo lo que necesita el navegador, SIN la categoría correcta de cada ficha."""
    ejercicio = EJERCICIOS[ejercicio_id]
    return {
        "enunciado": ejercicio["enunciado"],
        "categorias": CATEGORIAS,
        "fichas": fichas(ejercicio),
        "grafica": _grafica(ejercicio_id),
        "ayuda": ejercicio["ayuda"],
    }