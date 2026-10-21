"""
Ejercicios de desigualdades (CU-08).
Cada paso es una desigualdad; el alumno elige el intervalo correcto.
"""

EJERCICIOS = {
    "lineales": {
        "titulo": "Encuentra el intervalo",
        "instrucciones": "Resuelve cada desigualdad y elige la solución.",
        "bitcoins": 40,
        "pasos": [
            {"pregunta": "x + 4 < 10", "opciones": ["x < 6", "x > 6", "x < 14"], "respuesta": "x < 6",
             "pista": "Resta 4 de ambos lados."},
            {"pregunta": "3x − 4 ≤ 11", "opciones": ["x ≤ 5", "x ≥ 5", "x ≤ 7/3"], "respuesta": "x ≤ 5",
             "pista": "Suma 4 y luego divide entre 3."},
            {"pregunta": "−2x > 6", "opciones": ["x > −3", "x < −3", "x < 3"], "respuesta": "x < −3",
             "pista": "Al dividir entre un número negativo, el signo se voltea."},
        ],
    },
}


def datos_publicos(ejercicio):
    return {"pasos": [{"pregunta": p["pregunta"], "opciones": p["opciones"]} for p in ejercicio["pasos"]]}


def revisar_respuesta(ejercicio, paso, respuesta):
    try:
        paso = int(paso)
        datos = ejercicio["pasos"][paso]
    except (TypeError, ValueError, IndexError):
        return None, False, ""
    if respuesta.strip() == datos["respuesta"]:
        return paso, True, "Correcto."
    return paso, False, f"Incorrecto. {datos['pista']}"
