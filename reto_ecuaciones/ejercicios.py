"""
Ejercicios de ecuaciones lineales (CU-07): "Resolver ecuaciones lineales en una matriz".

El alumno restaura los valores perdidos (A a F) de un bloque de memoria de 3x3 usando
6 pistas. El navegador solo muestra la matriz y las pistas (que son públicas) y manda los
valores escritos; aquí, en el servidor, se valida que sean enteros y se evalúan las pistas.
Las pistas mismas nunca revelan la solución: solo relacionan unas celdas con otras.

Un ejercicio = lista de "pasos". Este reto tiene un solo paso (el alumno verifica toda la
matriz de una vez); views.py y progreso.servicios cuentan los pasos con len(pasos) y dan los
bitcoins cuando ese paso sale correcto (solo la primera vez que se completa el reto).
"""
import ast
import re

MENSAJE_INVALIDO = "Ingresaste valores no enteros, por favor corregir."
MENSAJE_INCORRECTO = "La respuesta es incorrecta."

# Un entero con signo, hasta 6 dígitos (suficiente para este ejercicio; evita
# que alguien mande un número absurdamente largo).
_ENTERO = re.compile(r"^-?\d{1,6}$")
# Cada pista es una condición escrita con referencias a la matriz, como la ve
# el alumno: "Matriz[0][0] + Matriz[0][1] == 14". Solo se permiten +, -, * y
# números — ver _evaluar().
_REFERENCIA_CELDA = re.compile(r"Matriz\[(\d)\]\[(\d)\]")

# Para cambiar el nivel solo hay que editar "matriz" y "pistas" de un ejercicio.
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
        # (Solución de referencia: [[10, 4, 16], [8, 12, 6], [14, 20, 2]])
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


# --- Lo que ve el navegador --------------------------------------------------

def _celdas_por_completar(ejercicio):
    """[{'nombre': 'A', 'fila': 0, 'col': 1}, ...] en el orden de la matriz."""
    return [
        {"nombre": valor, "fila": i, "col": j}
        for i, fila in enumerate(ejercicio["matriz"])
        for j, valor in enumerate(fila)
        if isinstance(valor, str)
    ]


def datos_publicos(ejercicio):
    """Lo que sí ve el navegador. Las pistas ya son públicas (se muestran); no hay solución."""
    return {
        "titulo": ejercicio["titulo"],
        "mision": ejercicio["mision"],
        "matriz": ejercicio["matriz"],
        "celdas": _celdas_por_completar(ejercicio),
        "pistas": list(ejercicio["pistas"]),
        "bitcoins": ejercicio["bitcoins"],
        # El navegador lo usa para distinguir "valores no válidos" (FA-2) de "pista incumplida" (FA-1).
        "mensaje_invalido": MENSAJE_INVALIDO,
        "mensaje_incorrecto": MENSAJE_INCORRECTO,
    }


# --- Leer la respuesta del alumno -------------------------------------------

def _leer_valores(ejercicio, respuesta):
    """Convierte 'A=4,B=16,...' en ({'A': 4, ...}, []), o en (None, [cajas por
    corregir]) si alguna caja vino vacía o con algo que no es un entero."""
    nombres = [celda["nombre"] for celda in _celdas_por_completar(ejercicio)]
    crudos = {}
    try:
        for par in str(respuesta).split(","):
            nombre, valor = par.split("=", 1)
            nombre = nombre.strip()
            if nombre in nombres and nombre not in crudos:
                crudos[nombre] = valor.strip()
    except ValueError:
        pass    # formato roto por completo: las cajas que no se alcanzaron a leer quedan "por corregir"

    por_corregir = [n for n in nombres if not _ENTERO.match(crudos.get(n, ""))]
    if por_corregir:
        return None, por_corregir
    return {n: int(crudos[n]) for n in nombres}, []


def _matriz_con_valores(ejercicio, valores):
    """La matriz completa (sin incógnitas), con lo que escribió el alumno."""
    return [
        [valores[celda] if isinstance(celda, str) else celda for celda in fila]
        for fila in ejercicio["matriz"]
    ]


# --- Evaluar las pistas -------------------------------------------------------

def _evaluar(nodo):
    """Evalúa un árbol de expresión con solo enteros, +, -, * y negación unaria
    (nada más se acepta — así una pista nunca puede ejecutar código arbitrario)."""
    if isinstance(nodo, ast.Constant) and type(nodo.value) is int:
        return nodo.value
    if isinstance(nodo, ast.UnaryOp) and isinstance(nodo.op, ast.USub):
        return -_evaluar(nodo.operand)
    if isinstance(nodo, ast.BinOp) and isinstance(nodo.op, (ast.Add, ast.Sub, ast.Mult)):
        izquierda, derecha = _evaluar(nodo.left), _evaluar(nodo.right)
        if isinstance(nodo.op, ast.Add):
            return izquierda + derecha
        if isinstance(nodo.op, ast.Sub):
            return izquierda - derecha
        return izquierda * derecha
    raise ValueError("expresión no permitida")


def _valor_de(expresion_texto, matriz):
    """Evalúa un lado de una pista (ya con las referencias a celdas sustituidas)."""
    sustituida = _REFERENCIA_CELDA.sub(
        lambda ref: f"({matriz[int(ref.group(1))][int(ref.group(2))]})",
        expresion_texto.strip(),
    )
    return _evaluar(ast.parse(sustituida, mode="eval").body)


def _pista_se_cumple(pista, matriz):
    izquierda, derecha = pista.split("==")
    return _valor_de(izquierda, matriz) == _valor_de(derecha, matriz)


def pistas_incumplidas(ejercicio, valores):
    """Números de pista (desde 1) que NO se cumplen con esos valores."""
    matriz = _matriz_con_valores(ejercicio, valores)
    return [n for n, pista in enumerate(ejercicio["pistas"], start=1) if not _pista_se_cumple(pista, matriz)]


# --- Entrada para views.py ----------------------------------------------------

def _enumerar(items):
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
    if valores is None:    # FA-2: cajas vacías o no enteras; no se llegan a evaluar las pistas
        return paso, False, f"{MENSAJE_INVALIDO} Cuadros por corregir: {_enumerar(por_corregir)}."

    incumplidas = pistas_incumplidas(ejercicio, valores)
    if incumplidas:    # FA-1: alguna pista no se cumple con esos valores
        etiqueta = "Pista que no se cumple" if len(incumplidas) == 1 else "Pistas que no se cumplen"
        return paso, False, f"{MENSAJE_INCORRECTO} {etiqueta}: {_enumerar(incumplidas)}."

    return paso, True, "Todas las pistas se cumplen."
