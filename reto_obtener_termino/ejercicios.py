"""
Ejercicios de "El término oculto" (CU-09), estilo Wordle.

Cada ejercicio es UN término oculto con su número de intentos. El alumno
escribe una palabra del mismo largo y el servidor le regresa el color de
cada letra:
    verde    -> la letra está en el término y en esa posición
    amarillo -> la letra está en el término pero en otra posición
    gris     -> la letra no está en el término (o ya se usaron todas sus apariciones)

El término y su significado NUNCA se mandan al navegador antes de tiempo:
datos_publicos() solo expone el largo, los intentos y la pista.

Para agregar términos de otra materia (Linux, Lógica, ...), agrega aquí el
ejercicio con nuevo_termino() y apúntalo en mapa/temas.py.
"""
import unicodedata

# Bitcoins según el largo del término (4 letras = 30, 5 = 40, 6 = 50, ...).
BITCOINS_BASE = 30
BITCOINS_POR_LETRA_EXTRA = 10

VERDE = "verde"
AMARILLO = "amarillo"
GRIS = "gris"


def bitcoins_por_largo(largo):
    return max(BITCOINS_BASE, BITCOINS_BASE + (largo - 4) * BITCOINS_POR_LETRA_EXTRA)


def nuevo_termino(titulo, termino, intentos, significado, pista=""):
    """Arma un ejercicio con los bitcoins calculados por el largo del término."""
    return {
        "titulo": titulo,
        "instrucciones": (
            "Descifra el término oculto. Verde: letra en su lugar. "
            "Amarillo: la letra está, pero en otro lugar. Gris: no está."
        ),
        "termino": termino,
        "intentos": intentos,
        "significado": significado,
        "pista": pista,
        "bitcoins": bitcoins_por_largo(len(termino)),
    }


EJERCICIOS = {
    # --- Introducción a la Programación · Conceptos básicos ---------------
    "conceptos-basicos-1": nuevo_termino(
        "El término oculto · Nivel 1", "DATO", 5,
        significado=(
            "Dato: representación de un valor (número, texto, booleano, etc.) "
            "que un programa almacena y procesa."
        ),
        pista="Es la materia prima que procesa cualquier programa.",
    ),
    "conceptos-basicos-2": nuevo_termino(
        "El término oculto · Nivel 2", "BUCLE", 4,
        significado=(
            "Bucle (ciclo): estructura que repite un bloque de instrucciones "
            "mientras se cumpla una condición, como for o while."
        ),
        pista="Sirve para repetir instrucciones.",
    ),
    "conceptos-basicos-3": nuevo_termino(
        "El término oculto · Nivel 3", "OBJETO", 3,
        significado=(
            "Objeto: instancia de una clase que agrupa datos (atributos) y "
            "comportamiento (métodos) en la programación orientada a objetos."
        ),
        pista="Se crea a partir de una clase.",
    ),

    # --- Lógica y Algoritmos · Conjuntos (el ejemplo original, ya como Wordle)
    "conjuntos": nuevo_termino(
        "El término oculto", "UNION", 5,
        significado="Unión (A ∪ B): conjunto con todos los elementos que están en A, en B o en ambos.",
        pista="Su símbolo es ∪.",
    ),
}


def normalizar(texto):
    """Mayúsculas, sin acentos ni espacios, para no castigar la ortografía."""
    texto = unicodedata.normalize("NFD", str(texto).strip().upper())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn" and not c.isspace())


def datos_publicos(ejercicio):
    """Lo único que ve el navegador: nada que revele el término."""
    return {
        "letras": len(ejercicio["termino"]),
        "intentos": ejercicio["intentos"],
        "pista": ejercicio["pista"],
    }


def colorear(intento, termino):
    """Colores de cada letra con el criterio de Wordle para letras repetidas:
    primero se marcan los verdes; luego cada amarillo "gasta" una aparición
    de esa letra en el término, así no se marcan más amarillos de los que hay."""
    colores = [GRIS] * len(intento)
    restantes = {}
    for i, (letra, correcta) in enumerate(zip(intento, termino)):
        if letra == correcta:
            colores[i] = VERDE
        else:
            restantes[correcta] = restantes.get(correcta, 0) + 1
    for i, letra in enumerate(intento):
        if colores[i] != VERDE and restantes.get(letra, 0) > 0:
            colores[i] = AMARILLO
            restantes[letra] -= 1
    return colores


def validar_intento(ejercicio, texto):
    """Regresa (intento_normalizado, error). error es "" si el intento es válido."""
    intento = normalizar(texto)
    largo = len(ejercicio["termino"])
    if len(intento) != largo:
        return intento, f"El término tiene {largo} letras."
    if not intento.isalpha():
        return intento, "Usa solo letras."
    return intento, ""


def revisar_intento(ejercicio, intento):
    """intento ya validado. Regresa (colores, correcto)."""
    termino = normalizar(ejercicio["termino"])
    return colorear(intento, termino), intento == termino
