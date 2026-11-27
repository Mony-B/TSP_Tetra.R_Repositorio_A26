"""Configuración y banco de retos de la batalla final (CU-13, R78-R82b).

Las respuestas correctas viven solo aquí: al navegador se manda únicamente
lo que devuelve `datos_publicos` (nunca la clave `respuesta`). Todos los
retos son de nivel avanzado y se mezclan de distintos tipos y materias; la
dificultad y el tiempo por tipo no cambian durante la batalla (R78, R78b).
"""

import random

# Vida del Kernel (R79): empieza en 100 % y la batalla se gana al llegar a 0 %.
VIDA_INICIAL = 100
DANO = 10  # reto superado: el Kernel pierde esta cantidad
CURA = 5  # reto fallado o tiempo agotado: el Kernel recupera esta cantidad

# Segundos por tipo de reto (R78b). Son fijos: no bajan con las rondas.
TIEMPO = {
    "opcion": 25,
    "orden": 40,
    "terminal": 30,
    "clasificar": 45,
}

# Margen para la latencia de red al validar el tiempo en el servidor.
GRACIA_SEGUNDOS = 2

TIPOS = {
    "opcion": "Responder pregunta",
    "orden": "Ordenar pasos",
    "terminal": "Terminal Linux",
    "clasificar": "Clasificar elementos",
}

# Formato de la clave `respuesta` según el tipo:
#   opcion      -> índice (int) de la opción correcta
#   orden       -> lista de pasos en el orden correcto
#   terminal    -> lista de comandos aceptados
#   clasificar  -> dict {elemento: índice de categoría}
RETOS = [
    {
        "tipo": "opcion",
        "materia": "Lógica",
        "enunciado": (
            "Con A = {2, 4, 6, 8} y B = {4, 8, 10}, ¿cuál es (A ∩ B) ∪ {1}?"
        ),
        "opciones": ["{4, 8}", "{1, 4, 8}", "{1, 2, 4, 6, 8, 10}", "{1, 10}"],
        "respuesta": 1,
    },
    {
        "tipo": "opcion",
        "materia": "Programación",
        "enunciado": (
            "¿Qué imprime?\n  x = 3\n  for i in range(2):\n"
            "      x = x * 2 - i\n  print(x)"
        ),
        "opciones": ["12", "10", "11", "6"],
        "respuesta": 2,
    },
    {
        "tipo": "opcion",
        "materia": "Lógica",
        "enunciado": "¿Qué expresión es equivalente a NOT (A AND B)?",
        "opciones": [
            "NOT A AND NOT B",
            "(NOT A) OR (NOT B)",
            "A OR B",
            "NOT A OR B",
        ],
        "respuesta": 1,
    },
    {
        "tipo": "orden",
        "materia": "Algoritmos",
        "enunciado": "Ordena los pasos de la búsqueda binaria en un arreglo ordenado.",
        "respuesta": [
            "Calcular el índice medio del rango",
            "Comparar el valor medio con el objetivo",
            "Descartar la mitad donde no puede estar",
            "Repetir con la mitad restante hasta encontrarlo o quedar sin elementos",
        ],
    },
    {
        "tipo": "orden",
        "materia": "Linux",
        "enunciado": (
            'Ordena los comandos para crear la carpeta "proyecto", entrar en ella, '
            'crear "notas.txt" y verificar que existe.'
        ),
        "respuesta": ["mkdir proyecto", "cd proyecto", "touch notas.txt", "ls"],
    },
    {
        "tipo": "terminal",
        "materia": "Linux",
        "enunciado": (
            "Estás en /home/alumno. Escribe el comando que lista TODOS los "
            "archivos (incluidos los ocultos) en formato largo."
        ),
        "directorio": "/home/alumno",
        "respuesta": ["ls -la", "ls -al", "ls -a -l", "ls -l -a"],
    },
    {
        "tipo": "terminal",
        "materia": "Linux",
        "enunciado": (
            "Crea de una sola vez la ruta docs/2026/notas, incluyendo las "
            "carpetas intermedias que no existan."
        ),
        "directorio": "/home/alumno",
        "respuesta": ["mkdir -p docs/2026/notas"],
    },
    {
        "tipo": "terminal",
        "materia": "Linux",
        "enunciado": (
            "Muestra solo las líneas que contienen la palabra error dentro de "
            "log.txt."
        ),
        "directorio": "/var/log",
        "respuesta": [
            "grep error log.txt",
            'grep "error" log.txt',
            "grep 'error' log.txt",
        ],
    },
    {
        "tipo": "clasificar",
        "materia": "Algoritmos",
        "enunciado": "Clasifica cada operación según su complejidad.",
        "categorias": ["O(1)", "O(n)", "O(n²)"],
        "respuesta": {
            "Leer arr[5]": 0,
            "Sumar todos los elementos de una lista": 1,
            "Comparar todos los pares de una lista": 2,
            "Obtener el primer elemento": 0,
            "Buscar un valor recorriendo una lista sin ordenar": 1,
            "Dos ciclos anidados de 0 a n": 2,
        },
    },
    {
        "tipo": "clasificar",
        "materia": "Sistemas operativos",
        "enunciado": "¿Qué corresponde al kernel y qué al espacio de usuario?",
        "categorias": ["Kernel", "Espacio de usuario"],
        "respuesta": {
            "Administrar la memoria": 0,
            "Planificar procesos": 0,
            "Controlador de disco": 0,
            "Navegador web": 1,
            "Editor de texto": 1,
            "Shell (bash)": 1,
        },
    },
]


def datos_publicos(indice):
    """Lo que el navegador puede ver del reto `indice`: sin la respuesta.

    Los pasos de "orden" y los elementos de "clasificar" salen mezclados.
    """
    reto = RETOS[indice]
    tipo = reto["tipo"]
    datos = {
        "tipo": tipo,
        "nombre_tipo": TIPOS[tipo],
        "materia": reto["materia"],
        "enunciado": reto["enunciado"],
        "tiempo": TIEMPO[tipo],
    }
    if tipo == "opcion":
        datos["opciones"] = reto["opciones"]
    elif tipo == "orden":
        datos["pasos"] = random.sample(reto["respuesta"], len(reto["respuesta"]))
    elif tipo == "terminal":
        datos["directorio"] = reto["directorio"]
    elif tipo == "clasificar":
        datos["categorias"] = reto["categorias"]
        elementos = list(reto["respuesta"])
        random.shuffle(elementos)
        datos["elementos"] = elementos
    return datos


def es_correcta(indice, respuesta):
    """Revisa en el servidor la respuesta enviada por el navegador."""
    reto = RETOS[indice]
    tipo = reto["tipo"]
    if tipo == "opcion":
        return type(respuesta) is int and respuesta == reto["respuesta"]
    if tipo == "orden":
        return respuesta == reto["respuesta"]
    if tipo == "terminal":
        if not isinstance(respuesta, str):
            return False
        return " ".join(respuesta.split()) in reto["respuesta"]
    if tipo == "clasificar":
        return respuesta == reto["respuesta"]
    return False
