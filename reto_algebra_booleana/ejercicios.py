"""
Ejercicios de álgebra booleana (CU-05): "Puertas lógicas".

El alumno mueve interruptores (p, q, ...) y presiona "Verificar". El navegador
solo manda el estado de los interruptores; aquí, en el servidor, se evalúa la
expresión. Las fórmulas viven solo en este archivo y nunca se mandan al navegador.

Un ejercicio = varias "puertas" (pasos). Cada paso es un circuito distinto; views.py y
progreso.servicios cuentan los pasos con len(pasos) y dan los bitcoins al terminar el último.
"""

EJERCICIOS = {
    "proposicional": {
        "titulo": "Puertas lógicas",
        "instrucciones": "Logra que el foco prenda interactuando con los interruptores.",
        "bitcoins": 50,   # se dan una sola vez, al completar las 3 puertas
        "pasos": [
            {
                "leyenda": "p ∨ ¬q",
                "operador": "∨",
                "variables": ["p", "q"],
                "inicial": {"p": 0, "q": 1},     # arranca en falso: el alumno debe moverlos
                "funcion": lambda v: bool(v["p"] or not v["q"]),
                "pista": "∨ (OR) vale 1 si al menos un lado es 1. Recuerda que ¬q invierte q: ¬q vale 1 cuando q = 0.",
            },
            {
                "leyenda": "¬q ∧ p",
                "operador": "∧",
                "variables": ["q", "p"],
                "inicial": {"p": 0, "q": 0},
                "funcion": lambda v: bool((not v["q"]) and v["p"]),
                "pista": "∧ (AND) necesita que ambos lados valgan 1: ¬q = 1 exige q = 0, y además p debe ser 1.",
            },
            {
                "leyenda": "¬p ∧ ¬q",
                "operador": "∧",
                "variables": ["p", "q"],
                "inicial": {"p": 1, "q": 1},
                "funcion": lambda v: bool((not v["p"]) and (not v["q"])),
                "pista": "Ambos lados deben valer 1, así que p y q deben ser 0 (De Morgan: ¬p ∧ ¬q = ¬(p ∨ q)).",
            },
        ],
    },
}


def datos_publicos(ejercicio):
    """Lo que sí ve el navegador (sin fórmulas ni respuestas)."""
    return {
        "instrucciones": ejercicio["instrucciones"],
        "pasos": [
            {
                "leyenda": p["leyenda"],
                "operador": p["operador"],
                "variables": p["variables"],
                "inicial": p["inicial"],
            }
            for p in ejercicio["pasos"]
        ],
    }


def _leer_estado(paso, respuesta):
    """Convierte 'p=1,q=0' en {'p': 1, 'q': 0}. Devuelve None si viene mal formado."""
    estado = {}
    try:
        for par in respuesta.split(","):
            nombre, valor = par.strip().split("=")
            nombre, valor = nombre.strip(), valor.strip()
            if valor not in ("0", "1") or nombre in estado:
                return None
            estado[nombre] = int(valor)
    except ValueError:
        return None
    if set(estado) != set(paso["variables"]):
        return None
    return estado


def revisar_respuesta(ejercicio, paso, respuesta):
    """Devuelve (paso, es_correcta, mensaje). Misma firma que usa views.revisar."""
    try:
        paso = int(paso)
        if paso < 0:
            raise IndexError
        datos = ejercicio["pasos"][paso]
    except (TypeError, ValueError, IndexError):
        return None, False, ""

    estado = _leer_estado(datos, respuesta)
    if estado is None:
        return paso, False, "No se pudo leer el estado de los interruptores. Intenta de nuevo."

    resumen = ", ".join(f"{n} = {v}" for n, v in estado.items())
    if datos["funcion"](estado):
        return paso, True, f"El circuito se cierra: con {resumen}, {datos['leyenda']} = 1."
    return paso, False, f"Con {resumen}, {datos['leyenda']} = 0. {datos['pista']}"
