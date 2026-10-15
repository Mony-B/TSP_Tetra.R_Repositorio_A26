"""
Exámenes: uno por materia (la llave es el slug de la materia) y la batalla
final ("final"). Las respuestas correctas solo viven aquí, en el servidor;
al navegador solo se mandan las preguntas y sus opciones.
"""

EXAMENES = {
    "logica": {
        "agente": "Agente LÓGICA",
        "tiempo_limite": 120,      # segundos
        "aciertos_minimos": 2,
        "bitcoins": 100,
        "preguntas": [
            {"texto": "p=1, q=0. ¿Cuánto vale p ∧ q?", "opciones": ["0", "1"], "respuesta": "0"},
            {"texto": "p=0, q=1. ¿Cuánto vale ¬p ∨ q?", "opciones": ["0", "1"], "respuesta": "1"},
            {"texto": "¿(A ∪ B)' = A' ∩ B'?", "opciones": ["Verdadero", "Falso"], "respuesta": "Verdadero"},
        ],
    },
    # Faltan: introprog, linux, calculo, algebra (mismo formato).

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
