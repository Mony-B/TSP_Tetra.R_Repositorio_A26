"""
Clasificar elementos por categorías (CU-08): contenido y reglas del reto.

El reto es reutilizable para cualquier materia: cada entrada de EJERCICIOS
define su enunciado, sus categorías y sus fichas; la mecánica (arrastrar cada
ficha a su caja) no cambia. Hay dos formas de dar el contenido, según "kind":

- "grafica" (Cálculo): la ficha es un punto (x, y) y la categoría correcta se
  calcula evaluando una desigualdad "y <op> f(x)" en el servidor (nunca se
  manda al navegador). Además de las cajas, se dibuja el plano cartesiano con
  la curva y la región sombreada.
- "generico" (cualquier otra materia): la ficha es una etiqueta de texto y
  cada una ya trae su categoría correcta en el propio ejercicio (tampoco se
  manda al navegador: fichas() la quita antes de exponerla). Sin gráfica.

Para agregar un subtema solo se agrega una entrada nueva; views.py y
juego.js no cambian con ninguno de los dos tipos.
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
        "kind": "grafica",
        "nivel": 1,
        "subtema": "Desigualdades lineales",
        "titulo": "Desigualdades lineales",
        "instrucciones": "Arrastra cada punto a la caja correcta: ¿cumple la desigualdad?",
        "enunciado": ["y ≥ 2x − 1"],
        "desigualdades": [{"op": ">=", "f": _lineal}],
        "puntos": [(0, 0), (1, 1), (-2, -3), (2, 1), (3, 2), (-1, -4)],
        "ayuda": "Sustituye x e y en la desigualdad. Si la línea es sólida, el punto sobre ella también cuenta.",
        "bitcoins": 30,
    },
    "cuadraticas": {
        "kind": "grafica",
        "nivel": 2,
        "subtema": "Desigualdades cuadráticas",
        "titulo": "Desigualdades cuadráticas",
        "instrucciones": "Arrastra cada punto a la caja correcta: ¿cumple la desigualdad?",
        "enunciado": ["y > x² − 4"],
        "desigualdades": [{"op": ">", "f": _parabola}],
        "puntos": [(0, 0), (3, 5), (1, -1), (2, -5), (0, -5), (-2, 4)],
        "ayuda": "Calcula x² − 4 con el valor de x. Con la línea punteada, el punto sobre la curva NO cuenta.",
        "bitcoins": 30,
    },
    "racionales": {
        "kind": "grafica",
        "nivel": 3,
        "subtema": "Desigualdades racionales",
        "titulo": "Desigualdades racionales",
        "instrucciones": "Arrastra cada punto a la caja correcta: ¿cumple la desigualdad?",
        "enunciado": ["y ≤ 2 / (x − 1)"],
        "desigualdades": [{"op": "<=", "f": _hiperbola}],
        "puntos": [(2, 1), (3, 0), (0, -1), (0, -3), (2, 3), (4, 1)],
        "ayuda": "Calcula 2 / (x − 1) con el valor de x y compara con y. Cuidado con el signo cuando x < 1.",
        "bitcoins": 30,
    },
    "compuestas": {
        "kind": "grafica",
        "nivel": 4,
        "subtema": "Desigualdades compuestas",
        "titulo": "Desigualdades compuestas",
        "instrucciones": "Un punto es solución solo si cumple las dos desigualdades a la vez.",
        "enunciado": ["y > x − 2", "y ≤ 4 − x²"],
        "desigualdades": [{"op": ">", "f": _recta}, {"op": "<=", "f": _parabola_invertida}],
        "puntos": [(0, 0), (1, 1), (-1, 3), (2, 0), (0, 5), (3, -1)],
        "ayuda": "Revisa cada desigualdad por separado; si falla una, el punto no es solución.",
        "bitcoins": 30,
    },
    # Cálculo · Funciones, gráficas y operaciones (Módulo 2 del temario).
    # Truco: dos desigualdades (<= y >=) con la misma f obligan a que el
    # punto quede EXACTAMENTE sobre la curva, así la mecánica "gráfica"
    # sirve para evaluar si un punto pertenece a la gráfica de f(x).
    "evaluacion-funciones": {
        "kind": "grafica",
        "nivel": 2,
        "subtema": "Funciones, gráficas y operaciones",
        "titulo": "¿Pertenece a la gráfica?",
        "instrucciones": "Arrastra cada punto a la caja correcta: ¿pertenece a la gráfica de la función?",
        "enunciado": ["y = x² − 4"],
        "desigualdades": [{"op": "<=", "f": _parabola}, {"op": ">=", "f": _parabola}],
        "puntos": [(-2, 0), (-1, -3), (0, -4), (1, 1), (0, 0), (3, 2)],
        "ayuda": "Sustituye x en f(x) = x² − 4. El punto pertenece a la gráfica solo si y es EXACTAMENTE igual a ese resultado.",
        "bitcoins": 30,
    },
    # Primer ejercicio "genérico" del catálogo real (sin gráfica): prueba de
    # que la mecánica sirve para otra materia, no solo Cálculo (ver
    # Temario_A26, 4.2 Introducción a la programación → Control de flujo).
    "condicionales-ciclos": {
        "kind": "generico",
        "nivel": 1,
        "subtema": "Control de flujo: condicionales y ciclos",
        "titulo": "Condicionales y ciclos",
        "instrucciones": "Arrastra cada ficha a la caja correcta: ¿es un condicional o un ciclo?",
        "enunciado": ["Clasifica cada palabra reservada de Python según si controla una decisión o una repetición."],
        "categorias": [
            {"id": "condicional", "nombre": "Condicional", "detalle": "(decide qué bloque ejecutar)"},
            {"id": "ciclo", "nombre": "Ciclo", "detalle": "(repite un bloque)"},
        ],
        "fichas": [
            {"etiqueta": "if", "categoria": "condicional"},
            {"etiqueta": "elif", "categoria": "condicional"},
            {"etiqueta": "else", "categoria": "condicional"},
            {"etiqueta": "while", "categoria": "ciclo"},
            {"etiqueta": "for", "categoria": "ciclo"},
            {"etiqueta": "break", "categoria": "ciclo"},
        ],
        "ayuda": "if/elif/else deciden qué bloque se ejecuta según una condición. while/for repiten un bloque; break también pertenece a un ciclo, porque lo interrumpe.",
        "bitcoins": 30,
    },
    # Álgebra · Números reales y sistemas de ecuaciones (Módulo 0 del temario).
    "conjuntos-numericos": {
        "kind": "generico",
        "nivel": 1,
        "subtema": "Números reales y sistemas de ecuaciones",
        "titulo": "Clasifica el número",
        "instrucciones": "Arrastra cada número a la caja de su conjunto.",
        "enunciado": ["Clasifica cada número según el conjunto numérico más específico al que pertenece."],
        "categorias": [
            {"id": "naturales", "nombre": "Naturales (ℕ)", "detalle": "(0, 1, 2, 3...)"},
            {"id": "enteros", "nombre": "Enteros (ℤ)", "detalle": "(incluye negativos)"},
            {"id": "racionales", "nombre": "Racionales (ℚ)", "detalle": "(fracciones exactas)"},
            {"id": "irracionales", "nombre": "Irracionales (𝕀)", "detalle": "(no se pueden escribir como fracción)"},
        ],
        "fichas": [
            {"etiqueta": "7", "categoria": "naturales"},
            {"etiqueta": "0", "categoria": "naturales"},
            {"etiqueta": "-5", "categoria": "enteros"},
            {"etiqueta": "-12", "categoria": "enteros"},
            {"etiqueta": "3/4", "categoria": "racionales"},
            {"etiqueta": "0.5", "categoria": "racionales"},
            {"etiqueta": "√2", "categoria": "irracionales"},
            {"etiqueta": "π", "categoria": "irracionales"},
        ],
        "ayuda": (
            "Naturales: 0, 1, 2, 3... Enteros: incluyen los negativos. "
            "Racionales: se pueden escribir como fracción exacta (a/b). "
            "Irracionales: su decimal no termina ni se repite, como √2 o π."
        ),
        "bitcoins": 30,
    },
    # Álgebra · Álgebra matricial y operaciones con matrices (Módulo 4 del temario).
    "tipos-de-matrices": {
        "kind": "generico",
        "nivel": 1,
        "subtema": "Álgebra matricial y operaciones con matrices",
        "titulo": "Clasifica la matriz",
        "instrucciones": "Arrastra cada matriz a la caja de su tipo.",
        "enunciado": ["Clasifica cada matriz según su tipo."],
        "categorias": [
            {"id": "cuadrada", "nombre": "Cuadrada", "detalle": "(mismo número de filas y columnas)"},
            {"id": "fila", "nombre": "Fila", "detalle": "(un solo renglón)"},
            {"id": "rectangular", "nombre": "Rectangular", "detalle": "(distinto número de filas y columnas)"},
            {"id": "simetrica", "nombre": "Simétrica", "detalle": "(igual a su transpuesta)"},
            {"id": "identidad", "nombre": "Identidad", "detalle": "(unos en la diagonal, ceros en el resto)"},
        ],
        "fichas": [
            {"etiqueta": "Matriz de 3×3 con números distintos por todos lados", "categoria": "cuadrada"},
            {"etiqueta": "Matriz de 2×2 con números distintos", "categoria": "cuadrada"},
            {"etiqueta": "Matriz de 1×4 (un solo renglón)", "categoria": "fila"},
            {"etiqueta": "Matriz de 2×5 (más columnas que filas)", "categoria": "rectangular"},
            {"etiqueta": "Matriz de 4×2 (más filas que columnas)", "categoria": "rectangular"},
            {"etiqueta": "Matriz cuadrada donde A[i][j] = A[j][i] para toda i, j", "categoria": "simetrica"},
            {"etiqueta": "Matriz de 3×3 que es igual a su propia transpuesta", "categoria": "simetrica"},
            {"etiqueta": "Matriz cuadrada con 1 en toda la diagonal principal y 0 en el resto", "categoria": "identidad"},
        ],
        "ayuda": (
            "Cuadrada: mismo número de filas y columnas. Fila: un solo renglón. "
            "Rectangular: filas y columnas distintas. Simétrica: A[i][j] = A[j][i] "
            "siempre (igual a su transpuesta). Identidad: 1 en la diagonal "
            "principal, 0 en todo lo demás."
        ),
        "bitcoins": 30,
    },
    # Lógica · Teoría de conjuntos y representación (Módulo 1 del temario).
    "tipos-de-conjuntos": {
        "kind": "generico",
        "nivel": 1,
        "subtema": "Teoría de conjuntos y representación",
        "titulo": "Clasifica el conjunto",
        "instrucciones": "Arrastra cada conjunto a la caja de su tipo.",
        "enunciado": ["Clasifica cada conjunto según su tipo."],
        "categorias": [
            {"id": "vacio", "nombre": "Vacío", "detalle": "(sin elementos)"},
            {"id": "unitario", "nombre": "Unitario", "detalle": "(un elemento)"},
            {"id": "binario", "nombre": "Binario", "detalle": "(dos elementos)"},
            {"id": "finito", "nombre": "Finito", "detalle": "(se pueden contar todos)"},
            {"id": "infinito", "nombre": "Infinito", "detalle": "(no tiene fin)"},
            {"id": "universal", "nombre": "Universal", "detalle": "(todo el dominio del problema)"},
        ],
        "fichas": [
            {"etiqueta": "{ }", "categoria": "vacio"},
            {"etiqueta": "∅", "categoria": "vacio"},
            {"etiqueta": "{Ciudad de México}", "categoria": "unitario"},
            {"etiqueta": "{rojo, azul}", "categoria": "binario"},
            {"etiqueta": "{1, 2, 3, 4, 5}", "categoria": "finito"},
            {"etiqueta": "{lunes, martes, miércoles, jueves, viernes, sábado, domingo}", "categoria": "finito"},
            {"etiqueta": "{0, 1, 2, 3, ...} (los naturales)", "categoria": "infinito"},
            {"etiqueta": "U = {todas las letras del abecedario} (en un ejercicio sobre letras)", "categoria": "universal"},
        ],
        "ayuda": (
            "Vacío: sin elementos. Unitario: un elemento. Binario: dos "
            "elementos. Finito: se pueden contar todos. Infinito: no tiene "
            "fin. Universal: contiene todo el dominio del problema."
        ),
        "bitcoins": 30,
    },
}


# --- Regla de clasificación (solo en el servidor) ---------------------------------

def _es_grafica(ejercicio):
    return ejercicio.get("kind", "grafica") == "grafica"


def es_solucion(ejercicio, x, y):
    for d in ejercicio["desigualdades"]:
        valor = d["f"](Fraction(x))
        if valor is None or not OPERADORES[d["op"]](Fraction(y), valor):
            return False
    return True


def categoria_correcta(ejercicio, indice):
    """La categoría correcta de la ficha en esa posición (nunca se manda al navegador)."""
    if _es_grafica(ejercicio):
        x, y = ejercicio["puntos"][indice]
        return SI if es_solucion(ejercicio, x, y) else NO
    return ejercicio["fichas"][indice]["categoria"]


def fichas(ejercicio):
    """Fichas con id estable (f0, f1, ...) según su posición en la lista.

    "grafica": la ficha es un punto (x, y). "generico": la ficha es una
    etiqueta de texto; su categoría correcta NUNCA se incluye aquí.
    """
    if _es_grafica(ejercicio):
        return [{"id": f"f{i}", "x": x, "y": y} for i, (x, y) in enumerate(ejercicio["puntos"])]
    return [{"id": f"f{i}", "etiqueta": f["etiqueta"]} for i, f in enumerate(ejercicio["fichas"])]


def evaluar_ficha(ejercicio, ficha_id, categoria):
    """Paso 5: ¿la ficha pertenece a la categoría elegida?

    Devuelve True / False, o None si la ficha o la categoría no existen.
    """
    categorias_validas = {c["id"] for c in ejercicio.get("categorias", CATEGORIAS)}
    if categoria not in categorias_validas:
        return None
    for indice, ficha in enumerate(fichas(ejercicio)):
        if ficha["id"] == ficha_id:
            return categoria_correcta(ejercicio, indice) == categoria
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
    """Todo lo que necesita el navegador, SIN la categoría correcta de cada ficha.

    "grafica" solo se incluye para los ejercicios tipo "grafica"; en los
    genéricos no hay plano cartesiano que dibujar.
    """
    ejercicio = EJERCICIOS[ejercicio_id]
    datos = {
        "enunciado": ejercicio["enunciado"],
        "categorias": ejercicio.get("categorias", CATEGORIAS),
        "fichas": fichas(ejercicio),
    }
    if _es_grafica(ejercicio):
        datos["grafica"] = _grafica(ejercicio_id)
    return datos