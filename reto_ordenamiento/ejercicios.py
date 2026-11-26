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
    # Lógica · Álgebra de proposiciones, formas normales y demostración (Módulo 4).
    "demostracion-induccion": {
        "titulo": "Algoritmo: demostración por inducción",
        "bitcoins": 30,
        "mision": (
            "Reconstruye los pasos para demostrar por inducción matemática "
            "que una propiedad se cumple para todos los números naturales."
        ),
        "pasos": [
            "Inicio",
            "Caso base: comprobar que la propiedad se cumple para el primer valor (n = 1 o n = 0)",
            "Hipótesis inductiva: suponer que la propiedad se cumple para un valor n = k",
            "Paso inductivo: demostrar que, si se cumple para k, también se cumple para k + 1",
            "Conclusión: la propiedad se cumple para todo número natural",
            "Fin",
        ],
        "orden_mostrado": [4, 1, 5, 2, 0, 3],
    },
    # Cálculo · Desigualdades compuestas (Módulo 1 del temario).
    "desigualdades-compuestas": {
        "titulo": "Algoritmo: resolver desigualdades compuestas",
        "bitcoins": 30,
        "mision": (
            "Reconstruye los pasos para resolver un sistema de dos "
            "desigualdades que deben cumplirse al mismo tiempo "
            "(y > x − 2 y y ≤ 4 − x²)."
        ),
        "pasos": [
            "Inicio",
            "Resolver o graficar la primera desigualdad por separado",
            "Resolver o graficar la segunda desigualdad por separado",
            "Identificar la región donde se traslapan las soluciones de ambas",
            "Marcar esa intersección como la región solución final",
            "Fin",
        ],
        "orden_mostrado": [2, 4, 0, 5, 1, 3],
    },
    # Cálculo · Derivación: regla de la cadena (Módulo 4 del temario).
    "regla-cadena": {
        "titulo": "Algoritmo: derivar con la regla de la cadena",
        "bitcoins": 30,
        "mision": (
            "Reconstruye los pasos para derivar una función compuesta "
            "usando la regla de la cadena."
        ),
        "pasos": [
            "Inicio",
            "Identificar la función externa y la función interna",
            "Derivar la función externa, dejando la interna sin tocar",
            "Derivar la función interna por separado",
            "Multiplicar la derivada externa por la derivada interna",
            "Fin",
        ],
        "orden_mostrado": [3, 0, 5, 2, 4, 1],
    },
    # Álgebra · Operaciones con polinomios y teoremas fundamentales (Módulo 1).
    "division-sintetica": {
        "titulo": "Algoritmo: división sintética",
        "bitcoins": 30,
        "mision": (
            "Reconstruye los pasos para dividir un polinomio entre (x − c) "
            "usando división sintética."
        ),
        "pasos": [
            "Inicio",
            "Escribir solo los coeficientes del polinomio, completando con 0 los términos que falten",
            "Bajar el primer coeficiente tal cual",
            "Multiplicar ese valor por c y sumarlo al siguiente coeficiente",
            "Repetir la multiplicación y suma hasta llegar al último coeficiente",
            "Fin (el último valor obtenido es el residuo, según el teorema del residuo)",
        ],
        "orden_mostrado": [3, 0, 5, 1, 4, 2],
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
