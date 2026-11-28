"""
Batalla Final contra el Kernel (caso de uso aparte -antes identificado como
CU15-, todavía sin desarrollar: su contenido es solo de ejemplo). Usa
"final" como única llave porque no es por materia (es contra las 5 a la
vez); las respuestas correctas solo viven aquí, en el servidor (ver
batalla/views.py).

Los exámenes finales por materia (CU-12, antes CU-04) ya no viven aquí:
se movieron a reto_examen_final_materia/ejercicios.py, con la misma
estructura que el resto de los retos (ver reto_algebra_booleana).
"""

EXAMENES = {
    "final": {
        "agente": "La IA",
        "tiempo_limite": 180,
        "aciertos_minimos": 3,
        "bitcoins": 300,
        "preguntas": [
            {"texto": "Las tres partes de un algoritmo son entrada, proceso y…", "opciones": ["salida", "ciclo", "variable"], "respuesta": "salida"},
            {"texto": "¿Qué comando muestra la carpeta actual en Linux?", "opciones": ["ls", "pwd", "cd"], "respuesta": "pwd"},
            {"texto": "Si 2x + 3 = 11, ¿cuánto vale x?", "opciones": ["4", "7", "5"], "respuesta": "4"},
            {"texto": "Si −2x > 6, entonces…", "opciones": ["x > −3", "x < −3", "x < 3"], "respuesta": "x < −3"},
        ],
    },
}
