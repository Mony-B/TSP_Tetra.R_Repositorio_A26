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

    # --- Lógica y Algoritmos · Relaciones y Venn ---------------------------
    "relaciones-venn": {
        "titulo": "Construir un diagrama de Venn",
        "bitcoins": 30,
        "mision": (
            "El panel de diagramas se desordenó. Reconstruye, en orden, los pasos "
            "para dibujar el diagrama de Venn de A ∪ B."
        ),
        "pasos": [
            "Dibuja el conjunto universal U como un rectángulo.",
            "Dibuja el círculo del conjunto A dentro de U.",
            "Dibuja el círculo del conjunto B traslapando al círculo de A.",
            "Sombrea la región que pertenece a A, a B, o a ambos.",
            "Esa región sombreada representa A ∪ B.",
        ],
        "orden_mostrado": [2, 4, 0, 3, 1],
    },

    # --- Lógica y Algoritmos · Álgebra de proposiciones y demostración -----
    "demostracion": {
        "titulo": "Demostración por inducción",
        "bitcoins": 30,
        "mision": (
            "Los apuntes de la demostración se revolvieron. Reconstruye en orden "
            "los pasos para probar por inducción que 1 + 2 + ... + n = n(n+1)/2."
        ),
        "pasos": [
            "Caso base: verifica que la fórmula se cumple para n = 1.",
            "Hipótesis inductiva: supón que la fórmula se cumple para n = k.",
            "Paso inductivo: demuestra que, si se cumple para k, también se cumple para k + 1.",
            "Concluye que la fórmula es válida para todo n ≥ 1.",
        ],
        "orden_mostrado": [2, 0, 3, 1],
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
