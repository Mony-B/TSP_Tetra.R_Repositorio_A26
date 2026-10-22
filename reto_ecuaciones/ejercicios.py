"""
Ejercicios de ecuaciones lineales (CU-07): "Resolver ecuaciones lineales en una matriz".

El alumno restaura los valores perdidos (A a F) de un bloque de memoria de 3x3 usando
6 pistas. El navegador solo muestra la matriz y las pistas (que son públicas) y manda los
valores escritos; aquí, en el servidor, se valida que sean enteros y se evalúan las pistas.

Un ejercicio = lista de "pasos". Este reto tiene un solo paso (el alumno verifica toda la
matriz de una vez); views.py y progreso.servicios cuentan los pasos con len(pasos) y dan los
bitcoins cuando ese paso sale correcto (solo la primera vez que se completa el reto).
"""
import ast
import re

# Cada pista es una condición escrita con referencias a la matriz, como la ve el alumno:
#   "Matriz[0][0] + Matriz[0][1] == 14"
# Se permiten +, -, * y números. Para cambiar el nivel solo hay que editar `matriz` y `pistas`.
MENSAJE_INVALIDO = "Ingresaste valores no enteros, por favor corregir."
MENSAJE_INCORRECTO = "La respuesta es incorrecta."
_ENTERO = re.compile(r"^-?\d{1,6}$")
_REF = re.compile(r"Matriz\[(\d)\]\[(\d)\]")

EJERCICIOS = {
    "lineales": {
        "titulo": "Resolver ecuaciones lineales en una matriz",
        "mision": (
            "El sistema de la estación central perdió la configuración de las válvulas de presión. "
            "Restaura los valores del bloque de memoria de 3x3 usando las pistas del sistema. "
            "Recuerda: en programación, los índices siempre comienzan en 0."
        ),
        "bitcoins": 50,   # se dan una sola vez, la primera vez que se completa el reto
        # Los textos son nombres de caja por completar; los números ya vienen resueltos.
        # (Solución: [[10, 4, 16], [8, 12, 6], [14, 20, 2]])
        "matriz": [
            [10, "A", "B"],
            ["C", 12, "D"],
            ["E", "F", 2],
        ],
        "pistas": [
            "Matriz[0][0] + Matriz[0][1] == 14",
            "Matriz[1][0] == Matriz[0][1] * 2",
            "Matriz[1][0] + Matriz[1][1] + Matriz[1][2] == 26",
            "Matriz[0][2] == Matriz[0][0] + Matriz[1][2]",
            "Matriz[2][1] == Matriz[0][0] * 2",
            "Matriz[2][0] == Matriz[2][1] - Matriz[1][2]",
        ],
        # Un solo paso: se verifica toda la matriz a la vez.
        "pasos": [{"nombre": "matriz"}],
    },
}


def _celdas(ejercicio):
    """Cajas por completar: [{'nombre': 'A', 'fila': 0, 'col': 1}, ...] en el orden de la matriz."""
    return [{"nombre": c, "fila": i, "col": j}
            for i, fila in enumerate(ejercicio["matriz"]) for j, c in enumerate(fila) if isinstance(c, str)]


def datos_publicos(ejercicio):
    """Lo que sí ve el navegador. Las pistas ya son públicas (se muestran); no hay solución."""
    return {
        "titulo": ejercicio["titulo"],
        "mision": ejercicio["mision"],
        "matriz": ejercicio["matriz"],
        "celdas": _celdas(ejercicio),
        "pistas": list(ejercicio["pistas"]),
        "bitcoins": ejercicio["bitcoins"],
        # El navegador lo usa para distinguir "valores no válidos" (FA-2) de "pista incumplida" (FA-1).
        "mensaje_invalido": MENSAJE_INVALIDO,
        "mensaje_incorrecto": MENSAJE_INCORRECTO,
    }


def _leer_valores(ejercicio, respuesta):
    """Convierte 'A=4,B=16,...' en ({'A': 4, ...}, [cajas por corregir]).
    Si hay cajas vacías o con algo que no es un entero, las lista."""
    nombres = [c["nombre"] for c in _celdas(ejercicio)]
    crudos = {}
    try:
        for par in str(respuesta).split(","):
            nombre, valor = par.split("=", 1)
            nombre = nombre.strip()
            if nombre in nombres and nombre not in crudos:
                crudos[nombre] = valor.strip()
    except ValueError:
        pass                      # formato roto: las cajas que no se leyeron salen como por corregir
    malas = [n for n in nombres if not _ENTERO.match(crudos.get(n, ""))]
    if malas:
        return None, malas
    return {n: int(crudos[n]) for n in nombres}, []


def _matriz_completa(ejercicio, valores):
    return [[valores[c] if isinstance(c, str) else c for c in fila] for fila in ejercicio["matriz"]]


def _evaluar(nodo):
    """Evalúa solo enteros con + - * (nada más se acepta)."""
    if isinstance(nodo, ast.Constant) and type(nodo.value) is int:
        return nodo.value
    if isinstance(nodo, ast.BinOp) and isinstance(nodo.op, (ast.Add, ast.Sub, ast.Mult)):
        izq, der = _evaluar(nodo.left), _evaluar(nodo.right)
        return izq + der if isinstance(nodo.op, ast.Add) else izq - der if isinstance(nodo.op, ast.Sub) else izq * der
    if isinstance(nodo, ast.UnaryOp) and isinstance(nodo.op, ast.USub):
        return -_evaluar(nodo.operand)
    raise ValueError("expresión no permitida")


def _cumple(pista, m):
    izq, der = pista.split("==")
    lado = lambda t: _evaluar(ast.parse(_REF.sub(lambda r: f"({m[int(r.group(1))][int(r.group(2))]})", t).strip(), mode="eval").body)
    return lado(izq) == lado(der)


def pistas_incumplidas(ejercicio, valores):
    """Números (desde 1) de las pistas que NO se cumplen con esos valores."""
    m = _matriz_completa(ejercicio, valores)
    return [i for i, p in enumerate(ejercicio["pistas"], start=1) if not _cumple(p, m)]


def _lista(items):
    items = [str(i) for i in items]
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " y " + items[-1]


def revisar_respuesta(ejercicio, paso, respuesta):
    """Devuelve (paso, es_correcta, mensaje). Misma firma que usa views.revisar."""
    try:
        paso = int(paso)
        if paso < 0:
            raise IndexError
        ejercicio["pasos"][paso]
    except (TypeError, ValueError, IndexError):
        return None, False, ""

    valores, por_corregir = _leer_valores(ejercicio, respuesta)
    if valores is None:                                   # FA-2: vacíos o no enteros; no se evalúan las pistas
        return paso, False, f"{MENSAJE_INVALIDO} Cuadros por corregir: {_lista(por_corregir)}."

    malas = pistas_incumplidas(ejercicio, valores)
    if malas:                                             # FA-1: alguna pista no se cumple
        etiqueta = "Pista que no se cumple" if len(malas) == 1 else "Pistas que no se cumplen"
        return paso, False, f"{MENSAJE_INCORRECTO} {etiqueta}: {_lista(malas)}."
    return paso, True, "Todas las pistas se cumplen."
