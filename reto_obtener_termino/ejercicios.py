"""
Ejercicios de obtener el término (CU-09).
Se muestran pistas y la cantidad de letras; el alumno escribe el término.
"""
import unicodedata

EJERCICIOS = {
    "conjuntos": {
        "titulo": "El término oculto",
        "instrucciones": "Recuperé fragmentos de un término. Escríbelo para descifrarlo.",
        "bitcoins": 40,
        "pasos": [
            {"pistas": ["Elementos que están en A y también en B.", "Su símbolo es ∩."],
             "respuesta": "interseccion"},
            {"pistas": ["Todos los elementos de A y de B juntos.", "Su símbolo es ∪."],
             "respuesta": "union"},
            {"pistas": ["Los elementos que NO están en el conjunto.", "Se escribe A'."],
             "respuesta": "complemento"},
        ],
    },
}


def _normalizar(texto):
    """Sin acentos, sin espacios y en minúsculas, para no castigar la ortografía."""
    texto = unicodedata.normalize("NFD", texto.strip().lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn" and not c.isspace())


def datos_publicos(ejercicio):
    return {"pasos": [{"pistas": p["pistas"], "letras": len(p["respuesta"])} for p in ejercicio["pasos"]]}


def revisar_respuesta(ejercicio, paso, respuesta):
    try:
        paso = int(paso)
        datos = ejercicio["pasos"][paso]
    except (TypeError, ValueError, IndexError):
        return None, False, ""
    if _normalizar(respuesta) == _normalizar(datos["respuesta"]):
        return paso, True, "Término descifrado."
    return paso, False, "Ese no es el término. Revisa las pistas."
