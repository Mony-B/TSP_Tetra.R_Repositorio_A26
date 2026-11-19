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
    # Linux · Rutas y jerarquía de directorios (Módulo 1 del temario).
    "rutas-jerarquia": {
        "titulo": "Laberinto de sombras: rutas",
        "bitcoins": 30,
        "preguntas": [
            {
                "texto": "Sector 1 de 3: ¿Cuál de estas es una ruta absoluta?",
                "opciones": ["documentos/notas.txt", "/home/alumno/documentos", "../documentos"],
                "respuesta": "/home/alumno/documentos",
            },
            {
                "texto": "Sector 2 de 3: ¿Qué símbolo representa tu carpeta personal (home)?",
                "opciones": ["~", "..", "."],
                "respuesta": "~",
            },
            {
                "texto": "Sector 3 de 3: ¿Qué comando te lleva un nivel arriba, al directorio padre?",
                "opciones": ["cd ..", "cd ~", "cd ."],
                "respuesta": "cd ..",
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
