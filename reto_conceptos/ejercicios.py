"""
Ejercicios de conceptos (CU-10): sopa de letras.
Se muestran las definiciones; el alumno encuentra cada concepto en la sopa.
La sopa se arma en el servidor y siempre sale igual para cada ejercicio.
"""
import random
import unicodedata

EJERCICIOS = {
    "algoritmos": {
        "titulo": "Conceptos de algoritmos",
        "instrucciones": "Encuentra el concepto de cada definición: toca la primera y la última letra.",
        "bitcoins": 30,
        "tamano": 10,
        "pasos": [
            {"palabra": "ALGORITMO", "definicion": "Serie de pasos ordenados para resolver un problema."},
            {"palabra": "ENTRADA", "definicion": "Los datos que recibe un algoritmo."},
            {"palabra": "PROCESO", "definicion": "Lo que el algoritmo hace con los datos."},
            {"palabra": "SALIDA", "definicion": "El resultado que entrega el algoritmo."},
        ],
    },
}

DIRECCIONES = [(0, 1), (1, 0), (1, 1)]  # derecha, abajo, diagonal
LETRAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _normalizar(texto):
    texto = unicodedata.normalize("NFD", texto.strip().upper())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn" and c.isalpha())


def armar_sopa(ejercicio, semilla="recode"):
    """Coloca las palabras en la cuadrícula y rellena con letras al azar."""
    n = ejercicio["tamano"]
    for intento in range(200):
        rnd = random.Random(f"{semilla}-{intento}")
        sopa = [[None] * n for _ in range(n)]
        ok = True
        for paso in ejercicio["pasos"]:
            palabra = _normalizar(paso["palabra"])
            colocada = False
            for _ in range(200):
                df, dc = rnd.choice(DIRECCIONES)
                f = rnd.randrange(n - df * (len(palabra) - 1))
                c = rnd.randrange(n - dc * (len(palabra) - 1))
                celdas = [(f + df * i, c + dc * i) for i in range(len(palabra))]
                if all(sopa[x][y] in (None, palabra[i]) for i, (x, y) in enumerate(celdas)):
                    for i, (x, y) in enumerate(celdas):
                        sopa[x][y] = palabra[i]
                    colocada = True
                    break
            if not colocada:
                ok = False
                break
        if ok:
            return ["".join(l or rnd.choice(LETRAS) for l in fila) for fila in sopa]
    raise ValueError("No se pudieron acomodar las palabras; agranda la sopa.")


def datos_publicos(ejercicio):
    # Se manda la sopa y las definiciones, pero no la lista de palabras.
    return {
        "sopa": armar_sopa(ejercicio),
        "pasos": [{"definicion": p["definicion"]} for p in ejercicio["pasos"]],
    }


def revisar_respuesta(ejercicio, paso, respuesta):
    """Aquí el paso lo decide el servidor: es la palabra que coincida."""
    seleccion = _normalizar(respuesta)
    for i, p in enumerate(ejercicio["pasos"]):
        palabra = _normalizar(p["palabra"])
        if seleccion in (palabra, palabra[::-1]):
            return i, True, f"Encontraste: {palabra}"
    return -1, False, "Eso no es ninguno de los conceptos."
