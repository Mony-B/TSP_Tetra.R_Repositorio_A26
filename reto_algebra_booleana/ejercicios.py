"""
Ejercicios de álgebra booleana (CU-05).
Cada paso es una expresión; el alumno elige el resultado o la forma simplificada.
"""

EJERCICIOS = {
    "proposicional": {
        "titulo": "Puertas lógicas",
        "instrucciones": "Las puertas solo abren con el valor correcto. Elige la respuesta de cada expresión.",
        "bitcoins": 50,
        "pasos": [
            {"pregunta": "p = 1, q = 0.  p ∧ q = ?", "opciones": ["0", "1"], "respuesta": "0",
             "pista": "∧ (AND) solo vale 1 si ambas son 1."},
            {"pregunta": "p = 0, q = 1.  ¬p ∨ q = ?", "opciones": ["0", "1"], "respuesta": "1",
             "pista": "Primero niega p; luego ∨ (OR) vale 1 si al menos una es 1."},
            {"pregunta": "Simplifica:  p ∧ 1", "opciones": ["p", "1", "0", "¬p"], "respuesta": "p",
             "pista": "Ley de identidad: AND con 1 no cambia el valor."},
            {"pregunta": "Simplifica:  p ∨ ¬p", "opciones": ["p", "1", "0", "¬p"], "respuesta": "1",
             "pista": "Ley del complemento: algo o su negación siempre es verdadero."},
        ],
    },
}


def datos_publicos(ejercicio):
    """Lo que sí ve el navegador (sin respuestas)."""
    return {"pasos": [{"pregunta": p["pregunta"], "opciones": p["opciones"]} for p in ejercicio["pasos"]]}


def revisar_respuesta(ejercicio, paso, respuesta):
    """Devuelve (paso, es_correcta, mensaje)."""
    try:
        paso = int(paso)
        datos = ejercicio["pasos"][paso]
    except (TypeError, ValueError, IndexError):
        return None, False, ""
    if respuesta.strip() == datos["respuesta"]:
        return paso, True, "Correcto. La puerta se abre."
    return paso, False, f"Incorrecto. {datos['pista']}"
