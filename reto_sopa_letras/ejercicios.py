"""
Ejercicios de conceptos (CU-10): sopa de letras.
Cada ejercicio tiene varios niveles; en cada uno se muestran las definiciones de
los conceptos y el alumno los encuentra en la sopa. El reto se completa al
terminar todos los niveles. Cada sopa se arma en el servidor y siempre sale igual.
"""

import random
import unicodedata

EJERCICIOS = {
    "algoritmos": {
        "titulo": "Conceptos de algoritmos",
        "instrucciones": (
            "Lee cada definición y encuentra el concepto en la sopa: arrastra "
            "sobre las letras o toca la primera y la última. Superas el reto "
            "cuando completas los tres niveles."
        ),
        "bitcoins": 30,
        "niveles": [
            {
                "tamano": 10,
                "semilla": "recode",
                "pasos": [
                    {
                        "palabra": "ALGORITMO",
                        "definicion": "Serie de pasos ordenados para resolver un problema.",
                    },
                    {
                        "palabra": "ENTRADA",
                        "definicion": "Los datos que recibe un algoritmo.",
                    },
                    {
                        "palabra": "PROCESO",
                        "definicion": "Lo que el algoritmo hace con los datos.",
                    },
                    {
                        "palabra": "SALIDA",
                        "definicion": "El resultado que entrega el algoritmo.",
                    },
                ],
            },
            {
                "tamano": 13,
                "semilla": "nivel2-2",
                "pasos": [
                    {
                        "palabra": "SECUENCIA",
                        "definicion": "Los pasos se ejecutan uno tras otro, en orden.",
                    },
                    {
                        "palabra": "DECISION",
                        "definicion": (
                            "Estructura que elige un camino según una pregunta "
                            "de sí o no."
                        ),
                    },
                    {
                        "palabra": "CICLO",
                        "definicion": "Estructura que repite un grupo de pasos.",
                    },
                    {
                        "palabra": "DIAGRAMA",
                        "definicion": (
                            "Dibujo con símbolos que representa los pasos de "
                            "un algoritmo."
                        ),
                    },
                    {
                        "palabra": "PSEUDOCODIGO",
                        "definicion": (
                            "Forma de escribir un algoritmo con palabras "
                            "parecidas al lenguaje humano."
                        ),
                    },
                ],
            },
            {
                "tamano": 14,
                "semilla": "nivel3-5",
                "pasos": [
                    {
                        "palabra": "VARIABLE",
                        "definicion": (
                            "Espacio con nombre donde se guarda un dato que "
                            "puede cambiar."
                        ),
                    },
                    {
                        "palabra": "CONDICION",
                        "definicion": "Expresión que solo puede ser verdadera o falsa.",
                    },
                    {
                        "palabra": "ITERACION",
                        "definicion": "Cada repetición de un ciclo.",
                    },
                    {
                        "palabra": "RECURSION",
                        "definicion": (
                            "Resolver un problema usando una versión más "
                            "pequeña del mismo problema."
                        ),
                    },
                    {
                        "palabra": "DEPURAR",
                        "definicion": "Buscar y corregir los errores de un algoritmo.",
                    },
                    {
                        "palabra": "COMPLEJIDAD",
                        "definicion": (
                            "Medida de cuánto tiempo o memoria necesita un "
                            "algoritmo."
                        ),
                    },
                ],
            },
        ],
    },
}

# Derecha, abajo y diagonal hacia abajo a la derecha.
DIRECCIONES = [(0, 1), (1, 0), (1, 1)]
LETRAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
MAX_INTENTOS_SOPA = 200


def _normalizar(texto):
    """Quita acentos, espacios y mayúsculas para comparar palabras."""
    texto = unicodedata.normalize("NFD", texto.strip().upper())
    return "".join(
        caracter
        for caracter in texto
        if unicodedata.category(caracter) != "Mn" and caracter.isalpha()
    )


def _celdas_de_palabra(fila, columna, direccion, largo):
    """Lista las celdas que ocuparía una palabra desde (fila, columna)."""
    salto_fila, salto_columna = direccion
    return [(fila + salto_fila * i, columna + salto_columna * i) for i in range(largo)]


def _colocar_palabra(cuadricula, palabra, azar):
    """Intenta poner la palabra en un lugar libre; devuelve si lo logró."""
    tamano = len(cuadricula)
    for _ in range(MAX_INTENTOS_SOPA):
        direccion = azar.choice(DIRECCIONES)
        fila = azar.randrange(tamano - direccion[0] * (len(palabra) - 1))
        columna = azar.randrange(tamano - direccion[1] * (len(palabra) - 1))
        celdas = _celdas_de_palabra(fila, columna, direccion, len(palabra))
        if all(
            cuadricula[fila_celda][columna_celda] in (None, palabra[i])
            for i, (fila_celda, columna_celda) in enumerate(celdas)
        ):
            for i, (fila_celda, columna_celda) in enumerate(celdas):
                cuadricula[fila_celda][columna_celda] = palabra[i]
            return True
    return False


def armar_sopa(nivel):
    """Coloca las palabras de un nivel en la cuadrícula y rellena con letras.

    Cada nivel tiene su propia semilla, así la sopa siempre sale igual.
    """
    semilla = nivel["semilla"]
    tamano = nivel["tamano"]
    for intento in range(MAX_INTENTOS_SOPA):
        azar = random.Random(f"{semilla}-{intento}")
        cuadricula = [[None] * tamano for _ in range(tamano)]
        palabras = [_normalizar(paso["palabra"]) for paso in nivel["pasos"]]
        if all(_colocar_palabra(cuadricula, palabra, azar) for palabra in palabras):
            return [
                "".join(letra or azar.choice(LETRAS) for letra in fila)
                for fila in cuadricula
            ]
    raise ValueError("No se pudieron acomodar las palabras; agranda la sopa.")


def total_pasos(ejercicio):
    """Cuenta los conceptos de todos los niveles; son los que completan el reto."""
    return sum(len(nivel["pasos"]) for nivel in ejercicio["niveles"])


def _inicio_de_nivel(ejercicio, nivel):
    """Número del primer concepto del nivel dentro de todo el reto."""
    return sum(len(n["pasos"]) for n in ejercicio["niveles"][:nivel])


def nivel_actual(ejercicio, encontrados):
    """Devuelve el nivel en el que va el alumno (el primero con conceptos sin encontrar)."""
    for numero, nivel in enumerate(ejercicio["niveles"]):
        inicio = _inicio_de_nivel(ejercicio, numero)
        if any(inicio + i not in encontrados for i in range(len(nivel["pasos"]))):
            return numero
    return len(ejercicio["niveles"])


def datos_publicos(ejercicio, numero=0):
    """Devuelve lo que ve el navegador de un nivel: la sopa y las definiciones.

    El alumno ve las definiciones (R20), pero no las palabras ni dónde están:
    el servidor es quien revisa cada selección.
    """
    nivel = ejercicio["niveles"][numero]
    return {
        "sopa": armar_sopa(nivel),
        "pasos": [{"definicion": paso["definicion"]} for paso in nivel["pasos"]],
        "nivel": numero + 1,
        "total_niveles": len(ejercicio["niveles"]),
    }


def palabra_de(ejercicio, indice):
    """Devuelve la palabra del concepto con ese número dentro de todo el reto."""
    for numero, nivel in enumerate(ejercicio["niveles"]):
        inicio = _inicio_de_nivel(ejercicio, numero)
        if inicio <= indice < inicio + len(nivel["pasos"]):
            return nivel["pasos"][indice - inicio]["palabra"]
    raise IndexError(indice)


def revisar_respuesta(ejercicio, numero, respuesta):
    """Busca la selección entre los conceptos del nivel actual.

    Devuelve (índice dentro de todo el reto, correcto, mensaje).
    """
    seleccion = _normalizar(respuesta)
    inicio = _inicio_de_nivel(ejercicio, numero)
    for indice, paso in enumerate(ejercicio["niveles"][numero]["pasos"]):
        palabra = _normalizar(paso["palabra"])
        # La selección puede hacerse de la primera a la última letra o al revés.
        if seleccion in (palabra, palabra[::-1]):
            return inicio + indice, True, f"Encontraste: {palabra}"
    return None, False, "Eso no es ninguno de los conceptos."
