"""
Cómo se ve cada materia en el mapa del campus: código de edificio,
texto de ambientación, posición sobre la imagen del mapa e imagen de vista
previa. Va aparte de temas.py porque esto es solo presentación.

x / y: posición del edificio en % de mapa/static/mapa/img/mapa_campus.jpg.
imagen: archivo en mapa/static/mapa/img/ (None = "señal no disponible").
villano: profe que custodia el edificio, controlado por MARÍA (None = aún sin definir).
aliado: quién ayuda al alumno en ese edificio.
"""

EDIFICIOS = {
    "introprog": {
        "codigo": "E-1",
        "desc": "Primer contacto.\nAquí comenzó todo. La IA tomó el campus y reescribió el conocimiento.\n"
                "Restaura este edificio para recuperar el control.",
        "x": 31, "y": 17, "imagen": "edificio_e1.jpg",
        "villano": "Prof. Zepeda", "aliado": "ADA",
    },
    "algebra": {
        "codigo": "E-2",
        "desc": "Las ecuaciones dejaron de cerrar.\nLas matrices del edificio se corrompieron y nada ocupa su lugar.\n"
                "Resuelve el sistema para estabilizarlo.",
        "x": 21, "y": 33, "imagen": "edificio_e2.jpg",
        "villano": None, "aliado": "RAFA",
    },
    "linux": {
        "codigo": "E-3",
        "desc": "La terminal sigue encendida.\nAlguien dejó procesos corriendo… y no son nuestros.\n"
                "Recupera los permisos de root.",
        "x": 81, "y": 26, "imagen": "edificio_e3.jpg",
        "villano": "Prof. Root", "aliado": "SUDO",  # nombres provisionales
    },
    "logica": {
        "codigo": "E-4",
        "desc": "Bucles sin salida.\nLos pasillos se repiten una y otra vez.\n"
                "Encuentra la condición de paro.",
        "x": 26.5, "y": 55, "imagen": None,  # falta la imagen de este edificio
        "villano": None, "aliado": "DANI",
    },
    "calculo": {
        "codigo": "E-5",
        "desc": "El límite no existe.\nEl edificio cambia con cada instante que pasa.\n"
                "Deriva el patrón antes de que diverja.",
        "x": 85, "y": 51, "imagen": "edificio_e5.jpg",
        "villano": None, "aliado": "KARIM",
    },
}

KERNEL = {
    "codigo": "KERNEL",
    "nombre": "Kernel",
    "desc": "El núcleo del sistema.\nDesde aquí MARÍA controla el campus y a cada profesor.\n"
            "Aprueba el examen de cada edificio para enfrentarla.",
    "x": 54.5, "y": 31, "imagen": "kernel.jpg",
    "villano": "MARÍA", "aliado": None,
}
