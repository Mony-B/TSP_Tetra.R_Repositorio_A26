"""
Responder preguntas explorando el laberinto (CU-14). El contenido
(preguntas, opciones y respuesta correcta) se configura por subtema sin
tocar la mecánica del laberinto (R70). El servidor nunca manda cuál de las
opciones es la correcta: solo el texto y las opciones de la pregunta
actual.
"""

EJERCICIOS = {
    "busqueda-avanzada": {
        "titulo": "Laberinto de sombras: Linux",
        "bitcoins": 30,
        "preguntas": [
            {
                "texto": "Sector 1 de 3: ¿Qué comando lista el contenido de la carpeta actual?",
                "opciones": ["pwd", "ls", "mv"],
                "respuesta": "ls",
            },
            {
                "texto": "Sector 2 de 3: ¿Qué comando muestra la ruta de la carpeta en la que estás?",
                "opciones": ["ls", "pwd", "chmod"],
                "respuesta": "pwd",
            },
            {
                "texto": "Sector 3 de 3: ¿Qué comando cambia los permisos de un archivo?",
                "opciones": ["grep", "chown", "chmod"],
                "respuesta": "chmod",
            },
        ],
    },

    # --- Lógica y Algoritmos · Algoritmos -----------------------------------
    "algoritmos": {
        "titulo": "Laberinto de sombras: Algoritmos",
        "bitcoins": 30,
        "preguntas": [
            {
                "texto": "Sector 1 de 3: ¿Qué parte de un algoritmo recibe los datos desde afuera?",
                "opciones": ["Proceso", "Entrada", "Salida"],
                "respuesta": "Entrada",
            },
            {
                "texto": "Sector 2 de 3: ¿Qué parte transforma los datos recibidos?",
                "opciones": ["Entrada", "Salida", "Proceso"],
                "respuesta": "Proceso",
            },
            {
                "texto": "Sector 3 de 3: ¿Qué parte entrega el resultado final?",
                "opciones": ["Proceso", "Salida", "Entrada"],
                "respuesta": "Salida",
            },
        ],
    },

    # --- Lógica y Algoritmos · Relaciones y Venn ----------------------------
    "relaciones-venn": {
        "titulo": "Laberinto de sombras: Conjuntos",
        "bitcoins": 30,
        "preguntas": [
            {
                "texto": "Sector 1 de 3: ¿Cómo se llama el conjunto con los elementos que están en A, en B, o en ambos?",
                "opciones": ["Intersección", "Unión", "Diferencia"],
                "respuesta": "Unión",
            },
            {
                "texto": "Sector 2 de 3: ¿Cómo se llama el conjunto con los elementos que están en A y en B a la vez?",
                "opciones": ["Unión", "Complemento", "Intersección"],
                "respuesta": "Intersección",
            },
            {
                "texto": "Sector 3 de 3: ¿Cómo se llama el conjunto con los elementos del universal que NO están en A?",
                "opciones": ["Diferencia", "Complemento", "Subconjunto"],
                "respuesta": "Complemento",
            },
        ],
    },

    # --- Lógica y Algoritmos · Lógica de programación -----------------------
    "logica-programacion": {
        "titulo": "Laberinto de sombras: Lógica de programación",
        "bitcoins": 30,
        "preguntas": [
            {
                "texto": "Sector 1 de 3: ¿Qué estructura repite un bloque de instrucciones?",
                "opciones": ["Condicional", "Bucle", "Función"],
                "respuesta": "Bucle",
            },
            {
                "texto": "Sector 2 de 3: ¿Cómo se llama una proposición que siempre es verdadera?",
                "opciones": ["Contradicción", "Tautología", "Variable"],
                "respuesta": "Tautología",
            },
            {
                "texto": "Sector 3 de 3: ¿Cómo se llama un bloque de código reutilizable que puede recibir parámetros?",
                "opciones": ["Clase", "Bucle", "Función"],
                "respuesta": "Función",
            },
        ],
    },
}


def total_pasos(ejercicio):
    return len(ejercicio["preguntas"])


def datos_publicos(ejercicio, numero):
    """Lo que ve el navegador de la pregunta actual: texto y opciones (sin
    marcar cuál es la correcta)."""
    pregunta = ejercicio["preguntas"][numero]
    return {
        "numero": numero + 1,
        "total": len(ejercicio["preguntas"]),
        "pregunta": pregunta["texto"],
        "opciones": list(pregunta["opciones"]),
    }


def revisar_respuesta(ejercicio, numero, respuesta):
    return respuesta == ejercicio["preguntas"][numero]["respuesta"]
