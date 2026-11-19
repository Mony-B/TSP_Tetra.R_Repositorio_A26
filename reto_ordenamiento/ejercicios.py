"""
Resolver reto de ordenamiento (CU-11): reconstruir un algoritmo acomodando
sus pasos sueltos en la línea de secuencia correcta.

Cada ejercicio define sus pasos en el orden correcto ("pasos") y el orden en
que se muestran desordenados ("orden_mostrado", fijo para que el reto
siempre salga igual). El servidor nunca manda cuál es el orden correcto: solo
los textos de los pasos y en qué posición de la línea se muestran.
"""

EJERCICIOS = {
    "par-impar": {
        "titulo": "Algoritmo: par o impar",
        "bitcoins": 30,
        "mision": (
            "El programa de control escolar se corrompió. Reconstruye el "
            "algoritmo que determina si un número es par o impar acomodando "
            "sus pasos en el orden correcto."
        ),
        "pasos": [
            "Inicio",
            "Declarar la variable N",
            "Leer el valor de N",
            "Calcular residuo ← N mod 2",
            'Si residuo = 0 mostrar "Par"; si no, mostrar "Impar"',
            "Fin",
        ],
        "orden_mostrado": [3, 5, 1, 4, 0, 2],
    },
    # Linux · Búsqueda avanzada (refuerzo): algoritmo de find + grep.
    "busqueda-eficiente": {
        "titulo": "Algoritmo: buscar sin leer todo",
        "bitcoins": 30,
        "mision": (
            "Reconstruye el algoritmo que te permite encontrar un texto entre "
            "muchos archivos sin tener que abrirlos todos uno por uno."
        ),
        "pasos": [
            "Inicio",
            "Elige en qué carpeta vas a empezar la búsqueda",
            "Usa find para localizar los archivos que podrían contener el texto",
            "Usa grep para filtrar solo las líneas que tienen el texto buscado",
            "Lee únicamente los resultados que grep ya filtró",
            "Fin",
        ],
        "orden_mostrado": [3, 0, 5, 1, 4, 2],
    },
    # Introprog · Datos y sentencias básicas (refuerzo, Módulo 1 del temario).
    "suma-dos-numeros": {
        "titulo": "Algoritmo: sumar dos números",
        "bitcoins": 30,
        "mision": (
            "Reconstruye el programa en Python que pide dos números al "
            "usuario y muestra su suma, acomodando sus pasos en el orden "
            "correcto."
        ),
        "pasos": [
            "Inicio",
            "Leer el primer número con input() y convertirlo a entero con int()",
            "Leer el segundo número con input() y convertirlo a entero con int()",
            "Calcular suma ← primer número + segundo número",
            "Mostrar el resultado con print()",
            "Fin",
        ],
        "orden_mostrado": [2, 5, 0, 4, 1, 3],
    },
}


def total_pasos(ejercicio):
    return len(ejercicio["pasos"])


def datos_publicos(ejercicio):
    """Lo que ve el navegador: la misión y los pasos desordenados (id + texto).
    Nunca se manda el orden correcto."""
    return {
        "mision": ejercicio["mision"],
        "pasos": [
            {"id": indice, "texto": ejercicio["pasos"][indice]}
            for indice in ejercicio["orden_mostrado"]
        ],
        "total": len(ejercicio["pasos"]),
    }


def verificar_secuencia(ejercicio, secuencia):
    """Recibe la lista de ids en cada posición de la línea (None = vacío).

    Devuelve (vacios, correcta):
      - vacios: posiciones (0-indexadas) todavía sin llenar (FA-2).
      - correcta: True si no hay vacíos y el orden coincide (ignorado si hay
        vacíos).
    """
    total = total_pasos(ejercicio)
    if len(secuencia) != total:
        # Secuencia mal formada: se trata como si estuviera toda vacía.
        return list(range(total)), False
    vacios = [i for i, valor in enumerate(secuencia) if valor is None]
    if vacios:
        return vacios, False
    correcta = all(valor == indice for indice, valor in enumerate(secuencia))
    return [], correcta
