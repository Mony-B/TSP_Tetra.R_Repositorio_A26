"""
Relacionar conceptos (CU-13): alinear tres carretes giratorios (concepto,
palabra clave, definición) para formar combinaciones válidas, en 3 rondas
de 3, 4 y 5 combinaciones. El banco de combinaciones se configura por
materia (R62b) sin tocar la mecánica.

Cada carrete se mezcla con una semilla fija (independiente para cada
columna), así el orden siempre sale igual pero las tres columnas no quedan
alineadas por posición: el alumno tiene que girar cada una por separado
para encontrar la combinación correcta.
"""
import random

EJERCICIOS = {
    "logica-programacion": {
        "titulo": "Relacionar conceptos",
        "bitcoins": 30,
        "semilla": "logica-programacion",
        "rondas": [
            [
                {"concepto": "Variable", "palabra": "var", "definicion": "Guarda un valor para usarlo después."},
                {"concepto": "Bucle", "palabra": "for / while", "definicion": "Repite un bloque de código varias veces."},
                {"concepto": "Función", "palabra": "def", "definicion": "Agrupa código para reutilizarlo."},
            ],
            [
                {"concepto": "Condicional", "palabra": "if / else", "definicion": "Ejecuta código según una condición."},
                {"concepto": "Arreglo", "palabra": "lista", "definicion": "Almacena varios elementos ordenados."},
                {"concepto": "Clase", "palabra": "class", "definicion": "Plantilla para crear objetos con datos y comportamiento."},
                {"concepto": "Constante", "palabra": "const", "definicion": "Valor que no cambia una vez asignado."},
            ],
            [
                {"concepto": "Recursión", "palabra": "llamada a sí misma", "definicion": "Una función que se invoca a sí misma para resolver un problema."},
                {"concepto": "Excepción", "palabra": "try / except", "definicion": "Manejo de errores que ocurren durante la ejecución."},
                {"concepto": "Comentario", "palabra": "#", "definicion": "Texto que el programa ignora, para explicar el código."},
                {"concepto": "Parámetro", "palabra": "argumento", "definicion": "Valor que se le pasa a una función al llamarla."},
                {"concepto": "Booleano", "palabra": "True / False", "definicion": "Tipo de dato con solo dos valores posibles."},
            ],
        ],
    },
}


def total_rondas(ejercicio):
    return len(ejercicio["rondas"])


def _mezclar(lista, semilla):
    azar = random.Random(semilla)
    copia = list(lista)
    azar.shuffle(copia)
    return copia


def datos_publicos(ejercicio):
    """Las tres columnas de cada ronda, mezcladas de forma independiente
    (misma semilla siempre, para que el reto salga igual). Nunca se manda
    qué índice de cada columna forma una combinación válida."""
    rondas = []
    for numero, combos in enumerate(ejercicio["rondas"]):
        base = f"{ejercicio['semilla']}-{numero}"
        rondas.append({
            "conceptos": _mezclar([c["concepto"] for c in combos], base + "-concepto"),
            "palabras": _mezclar([c["palabra"] for c in combos], base + "-palabra"),
            "definiciones": _mezclar([c["definicion"] for c in combos], base + "-definicion"),
            "total": len(combos),
        })
    return {"rondas": rondas, "total_rondas": len(rondas)}


def verificar_combinacion(ejercicio, numero_ronda, concepto, palabra, definicion):
    """True si (concepto, palabra, definicion) es una de las combinaciones
    válidas de esa ronda (sin importar en qué posición de carrete esté)."""
    if not (0 <= numero_ronda < len(ejercicio["rondas"])):
        return False
    return any(
        combo["concepto"] == concepto and combo["palabra"] == palabra and combo["definicion"] == definicion
        for combo in ejercicio["rondas"][numero_ronda]
    )
