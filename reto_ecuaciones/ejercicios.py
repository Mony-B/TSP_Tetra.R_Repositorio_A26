"""
Ejercicios de ecuaciones (CU-07).
El alumno escribe el valor de x; se compara como número en el servidor.
"""
from fractions import Fraction

EJERCICIOS = {
    "lineales": {
        "titulo": "Resuelve para x",
        "instrucciones": "Escribe el valor de x (puede ser entero, decimal o fracción como 3/4).",
        "bitcoins": 40,
        "pasos": [
            {"ecuacion": "2x + 3 = 11", "respuesta": "4", "pista": "Resta 3 y luego divide entre 2."},
            {"ecuacion": "5x − 7 = 3x + 9", "respuesta": "8", "pista": "Junta las x de un lado y los números del otro."},
            {"ecuacion": "x/3 + 2 = 6", "respuesta": "12", "pista": "Resta 2 y luego multiplica por 3."},
        ],
    },
}


def datos_publicos(ejercicio):
    return {"pasos": [{"ecuacion": p["ecuacion"]} for p in ejercicio["pasos"]]}


def _a_numero(texto):
    texto = texto.strip().lower().replace(" ", "").replace("x=", "").replace(",", ".").replace("−", "-")
    try:
        return Fraction(texto)
    except (ValueError, ZeroDivisionError):
        return None


def revisar_respuesta(ejercicio, paso, respuesta):
    try:
        paso = int(paso)
        datos = ejercicio["pasos"][paso]
    except (TypeError, ValueError, IndexError):
        return None, False, ""
    valor = _a_numero(respuesta)
    if valor is None:
        return paso, False, "Escribe un número, por ejemplo 4, 2.5 o 3/4."
    if valor == Fraction(datos["respuesta"]):
        return paso, True, "Correcto."
    return paso, False, f"Ese no es el valor de x. {datos['pista']}"
