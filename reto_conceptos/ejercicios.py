"""
Ejercicios de conceptos (CU-10): sopa de letras.
Se muestra la lista de conceptos del subtema y el alumno los encuentra en la sopa.
La sopa se arma en el servidor y siempre sale igual para cada ejercicio.
"""

import random
import unicodedata

EJERCICIOS = {
    "algoritmos": {
        "titulo": "Conceptos de algoritmos",
        "instrucciones": (
            "Encuentra los conceptos de la lista: arrastra sobre las letras "
            "o toca la primera y la última."
        ),
        "bitcoins": 30,
        "tamano": 10,
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


def armar_sopa(ejercicio, semilla="recode"):
    """Coloca las palabras en la cuadrícula y rellena con letras al azar."""
    tamano = ejercicio["tamano"]
    for intento in range(MAX_INTENTOS_SOPA):
        azar = random.Random(f"{semilla}-{intento}")
        cuadricula = [[None] * tamano for _ in range(tamano)]
        palabras = [_normalizar(paso["palabra"]) for paso in ejercicio["pasos"]]
        if all(_colocar_palabra(cuadricula, palabra, azar) for palabra in palabras):
            return [
                "".join(letra or azar.choice(LETRAS) for letra in fila)
                for fila in cuadricula
            ]
    raise ValueError("No se pudieron acomodar las palabras; agranda la sopa.")


def datos_publicos(ejercicio):
    """Devuelve lo que ve el navegador: la sopa y la lista de conceptos.

    La lista se muestra al alumno (R20), pero no se manda dónde está cada palabra:
    el servidor es quien revisa cada selección.
    """
    return {
        "sopa": armar_sopa(ejercicio),
        "pasos": [
            {"palabra": paso["palabra"], "definicion": paso["definicion"]}
            for paso in ejercicio["pasos"]
        ],
    }


def revisar_respuesta(ejercicio, respuesta):
    """Busca la selección entre los conceptos y devuelve (índice, correcto, mensaje)."""
    seleccion = _normalizar(respuesta)
    for indice, paso in enumerate(ejercicio["pasos"]):
        palabra = _normalizar(paso["palabra"])
        # La selección puede hacerse de la primera a la última letra o al revés.
        if seleccion in (palabra, palabra[::-1]):
            return indice, True, f"Encontraste: {palabra}"
    return None, False, "Eso no es ninguno de los conceptos."
