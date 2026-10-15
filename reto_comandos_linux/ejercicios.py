"""
Ejercicios de comandos de Linux (CU-06).
Cada paso es una tarea; el alumno escribe el comando en una terminal simulada.
"""

EJERCICIOS = {
    "basicos": {
        "titulo": "Navega la terminal",
        "instrucciones": "La red te dejó en una terminal. Escribe el comando que pide cada tarea.",
        "bitcoins": 50,
        "pasos": [
            {"tarea": "Muestra en qué carpeta estás.",
             "aceptadas": ["pwd"],
             "salida": "/home/alumno",
             "pista": "Es la abreviatura de 'print working directory'."},
            {"tarea": "Lista los archivos de la carpeta.",
             "aceptadas": ["ls", "ls -l", "ls -a", "ls -la", "ls -al"],
             "salida": "notas.txt  secretos/",
             "pista": "Es un comando de dos letras que 'lista'."},
            {"tarea": "Entra a la carpeta secretos.",
             "aceptadas": ["cd secretos", "cd secretos/", "cd ./secretos"],
             "salida": "",
             "pista": "Usa 'cd' seguido del nombre de la carpeta."},
            {"tarea": "Crea un archivo vacío llamado pista.txt.",
             "aceptadas": ["touch pista.txt"],
             "salida": "",
             "pista": "El comando 'toca' el archivo para crearlo."},
        ],
    },
}


def datos_publicos(ejercicio):
    return {"pasos": [{"tarea": p["tarea"]} for p in ejercicio["pasos"]]}


def _normalizar(comando):
    return " ".join(comando.strip().split())


def revisar_respuesta(ejercicio, paso, respuesta):
    try:
        paso = int(paso)
        datos = ejercicio["pasos"][paso]
    except (TypeError, ValueError, IndexError):
        return None, False, ""
    if _normalizar(respuesta) in datos["aceptadas"]:
        return paso, True, datos["salida"] or "✓"
    comando = _normalizar(respuesta).split(" ")[0] or "?"
    return paso, False, f"{comando}: no hace lo que se pide. {datos['pista']}"
