"""
Exámenes: uno por materia (la llave es el slug de la materia) y la batalla
final ("final", CU15 -todavía sin desarrollar: su contenido es de ejemplo).
Las respuestas correctas solo viven aquí, en el servidor; al navegador
solo se mandan las preguntas y sus opciones (ver batalla/views.py).

CU04 (SRS R39-R43, R73-R75): cada examen de materia son 15 preguntas de
opción múltiple, temporizador de 3 min 30 s (210 s), se aprueba con al
menos 10 de las 15 correctas, y otorga 60 bitcoins solo la primera vez
que se aprueba (progreso.servicios.registrar_examen ya se encarga de
eso). Las 15 preguntas de cada materia reparten entre los mismos
subtemas de mapa/temas.py, para cubrir todo lo que esa materia enseña y
no solo lo que ya tiene reto.
"""

TIEMPO_LIMITE = 210        # 3:30, igual para las 5 materias (R39/R73)
ACIERTOS_MINIMOS = 10      # de 15 (R41/R73)
BITCOINS_EXAMEN = 60       # solo la primera vez que se aprueba (R42/R73)

EXAMENES = {
    "logica": {
        "agente": "Agente LÓGICA",
        "tiempo_limite": TIEMPO_LIMITE,
        "aciertos_minimos": ACIERTOS_MINIMOS,
        "bitcoins": BITCOINS_EXAMEN,
        "preguntas": [
            # Teoría de conjuntos y representación
            {"texto": "¿Cuántos elementos tiene el conjunto vacío (∅)?",
             "opciones": ["0", "1", "Infinitos"], "respuesta": "0"},
            {"texto": "Un conjunto que tiene exactamente un elemento se llama:",
             "opciones": ["Unitario", "Vacío", "Finito"], "respuesta": "Unitario"},
            # Relaciones, operaciones y Venn
            {"texto": "Si A = {1, 2, 3} y B = {3, 4, 5}, ¿cuánto vale A ∪ B?",
             "opciones": ["{1, 2, 3, 4, 5}", "{3}", "{1, 2, 4, 5}"], "respuesta": "{1, 2, 3, 4, 5}"},
            {"texto": "Si A = {1, 2, 3} y B = {2, 3, 4}, ¿cuánto vale A ∩ B?",
             "opciones": ["{2, 3}", "{1, 4}", "{1, 2, 3, 4}"], "respuesta": "{2, 3}"},
            {"texto": "Si A = {1, 2, 3} y B = {2, 3}, ¿cuánto vale A − B?",
             "opciones": ["{1}", "{2, 3}", "{}"], "respuesta": "{1}"},
            {"texto": "Si A = {1, 2} y B = {1, 2, 3}, ¿cuál afirmación es verdadera?",
             "opciones": ["A ⊆ B", "B ⊆ A", "A = B"], "respuesta": "A ⊆ B"},
            # Lógica proposicional y tablas de verdad
            {"texto": "p = 1, q = 0. ¿Cuánto vale p ∧ q?", "opciones": ["0", "1"], "respuesta": "0"},
            {"texto": "p = 0, q = 1. ¿Cuánto vale ¬p ∨ q?", "opciones": ["1", "0"], "respuesta": "1"},
            {"texto": "p = 1, q = 0. ¿Cuánto vale p → q (condicional)?", "opciones": ["0", "1"], "respuesta": "0"},
            {"texto": "Una proposición que siempre es verdadera, sin importar los valores de sus variables, se llama:",
             "opciones": ["Tautología", "Contradicción", "Contingencia"], "respuesta": "Tautología"},
            # Álgebra de proposiciones y demostración
            {"texto": "Según las leyes de De Morgan, ¬(p ∧ q) equivale a:",
             "opciones": ["¬p ∨ ¬q", "¬p ∧ ¬q", "p ∨ q"], "respuesta": "¬p ∨ ¬q"},
            {"texto": "Una expresión escrita como una disyunción (OR) de conjunciones (AND) de literales está en:",
             "opciones": ["Forma normal disyuntiva (FND)", "Forma normal conjuntiva (FNC)", "Forma canónica única"],
             "respuesta": "Forma normal disyuntiva (FND)"},
            {"texto": "En una demostración por inducción matemática, el primer paso es:",
             "opciones": ["Probar el caso base", "Suponer que es falsa", "Probar el caso n+1 sin más"],
             "respuesta": "Probar el caso base"},
            {"texto": "La notación O(n²) describe:",
             "opciones": ["La complejidad de un algoritmo", "El número de variables de un programa", "Un tipo de dato"],
             "respuesta": "La complejidad de un algoritmo"},
            {"texto": "¿Cuál de las siguientes es una característica obligatoria de todo algoritmo?",
             "opciones": ["Ser finito (terminar en algún momento)", "Usar solo números", "Ejecutarse en menos de un segundo"],
             "respuesta": "Ser finito (terminar en algún momento)"},
        ],
    },
    "introprog": {
        "agente": "Agente INTROPROG",
        "tiempo_limite": TIEMPO_LIMITE,
        "aciertos_minimos": ACIERTOS_MINIMOS,
        "bitcoins": BITCOINS_EXAMEN,
        "preguntas": [
            # Fundamentos de computación y herramientas
            {"texto": "¿Qué hace la función print() en Python?",
             "opciones": ["Muestra un valor en la terminal", "Lee un valor del usuario", "Declara una variable"],
             "respuesta": "Muestra un valor en la terminal"},
            {"texto": "Un programa que traduce todo el código fuente a código máquina antes de ejecutarlo se llama:",
             "opciones": ["Compilador", "Intérprete", "Editor"], "respuesta": "Compilador"},
            {"texto": "¿Qué función de Python pausa el programa y espera a que el usuario escriba algo?",
             "opciones": ["input()", "print()", "return()"], "respuesta": "input()"},
            # Datos y sentencias básicas
            {"texto": "¿Cuál de los siguientes es un valor del tipo booleano?",
             "opciones": ["True", '"True"', "1.0"], "respuesta": "True"},
            {"texto": "x = 5; y = 2. ¿Cuánto vale x + y * 2?",
             "opciones": ["9", "14", "7"], "respuesta": "9"},
            # Sentencias condicionales
            {"texto": "x = 5. ¿Qué se imprime con: if x > 10: print('A')\\nelif x > 3: print('B')\\nelse: print('C')?",
             "opciones": ["B", "A", "C"], "respuesta": "B"},
            {"texto": "¿Qué estructura ejecuta un bloque de código si una condición es verdadera y otro distinto si es falsa?",
             "opciones": ["if / else", "while", "def"], "respuesta": "if / else"},
            # Ciclos y arreglos
            {"texto": "Un ciclo while repite su bloque de código:",
             "opciones": ["Mientras la condición siga siendo verdadera", "Un número fijo de veces siempre", "Solo una vez"],
             "respuesta": "Mientras la condición siga siendo verdadera"},
            {"texto": "En Python, ¿cuál es el índice del primer elemento de una lista?",
             "opciones": ["0", "1", "-1"], "respuesta": "0"},
            {"texto": "lista = [10, 20, 30]. ¿Qué vale lista[1]?",
             "opciones": ["20", "10", "30"], "respuesta": "20"},
            # Subrutinas y programación modular
            {"texto": "A diferencia de un procedimiento, una función:",
             "opciones": ["Regresa un valor al código que la llamó", "Nunca recibe parámetros", "No puede llamarse más de una vez"],
             "respuesta": "Regresa un valor al código que la llamó"},
            {"texto": "Una variable definida dentro de una función, por defecto:",
             "opciones": ["Solo existe dentro de esa función (ámbito local)", "Es visible en todo el programa", "Se vuelve constante"],
             "respuesta": "Solo existe dentro de esa función (ámbito local)"},
            # Introducción a POO
            {"texto": "Una clase es:",
             "opciones": ["Una plantilla para crear objetos", "Un objeto ya creado", "Un tipo de ciclo"],
             "respuesta": "Una plantilla para crear objetos"},
            {"texto": "Cuando una clase toma los atributos y métodos de otra clase, a eso se le llama:",
             "opciones": ["Herencia", "Encapsulación", "Composición"], "respuesta": "Herencia"},
            {"texto": "En Python, el método especial que se ejecuta automáticamente al crear un objeto nuevo se llama:",
             "opciones": ["__init__", "__new__", "__main__"], "respuesta": "__init__"},
        ],
    },
    "linux": {
        "agente": "Agente LINUX",
        "tiempo_limite": TIEMPO_LIMITE,
        "aciertos_minimos": ACIERTOS_MINIMOS,
        "bitcoins": BITCOINS_EXAMEN,
        "preguntas": [
            # Exploración del entorno
            {"texto": "¿Qué comando muestra la ruta de la carpeta en la que te encuentras?",
             "opciones": ["pwd", "ls", "cd"], "respuesta": "pwd"},
            {"texto": "¿Qué comando lista los archivos y carpetas de la carpeta actual?",
             "opciones": ["ls", "cat", "mkdir"], "respuesta": "ls"},
            {"texto": "¿Qué comando limpia la pantalla de la terminal sin afectar el historial de comandos?",
             "opciones": ["clear", "rm", "exit"], "respuesta": "clear"},
            # Rutas y jerarquía
            {"texto": "Una ruta que empieza desde la raíz (/), sin importar en qué carpeta estés parado, se llama:",
             "opciones": ["Ruta absoluta", "Ruta relativa", "Ruta temporal"], "respuesta": "Ruta absoluta"},
            {"texto": "Dentro de una ruta, '..' representa:",
             "opciones": ["La carpeta anterior (el padre)", "La carpeta actual", "La raíz del sistema"],
             "respuesta": "La carpeta anterior (el padre)"},
            # Creación y manipulación de archivos
            {"texto": "¿Qué comando crea una carpeta nueva?",
             "opciones": ["mkdir", "touch", "rm"], "respuesta": "mkdir"},
            {"texto": "¿Qué comando copia un archivo a otra ubicación sin borrar el original?",
             "opciones": ["cp", "mv", "rm"], "respuesta": "cp"},
            # Lectura de bitácoras
            {"texto": "¿Qué comando muestra las últimas líneas de un archivo, y con -f sigue mostrando nuevas en tiempo real?",
             "opciones": ["tail", "head", "cat"], "respuesta": "tail"},
            # Búsqueda avanzada
            {"texto": "¿Qué comando busca líneas que coincidan con un patrón de texto dentro de un archivo?",
             "opciones": ["grep", "find", "ls"], "respuesta": "grep"},
            {"texto": "¿Qué operador conecta la salida de un comando con la entrada de otro?",
             "opciones": ["| (tubería)", ">", "&&"], "respuesta": "| (tubería)"},
            # Permisos y propiedad
            {"texto": "¿Qué comando cambia los permisos de lectura, escritura y ejecución de un archivo?",
             "opciones": ["chmod", "chown", "su"], "respuesta": "chmod"},
            {"texto": "¿Qué comando cambia el dueño de un archivo o carpeta?",
             "opciones": ["chown", "chmod", "ps"], "respuesta": "chown"},
            {"texto": "¿Qué comando permite cambiar de usuario dentro de la misma sesión de terminal?",
             "opciones": ["su", "cd", "whoami"], "respuesta": "su"},
            # Procesos
            {"texto": "¿Qué comando muestra los procesos que están corriendo actualmente en el sistema?",
             "opciones": ["ps", "pwd", "df -h"], "respuesta": "ps"},
            {"texto": "¿Qué combinación de teclas interrumpe el proceso que corre en primer plano en la terminal?",
             "opciones": ["Ctrl+C", "Ctrl+V", "Ctrl+Z"], "respuesta": "Ctrl+C"},
        ],
    },
    "calculo": {
        "agente": "Agente CÁLCULO",
        "tiempo_limite": TIEMPO_LIMITE,
        "aciertos_minimos": ACIERTOS_MINIMOS,
        "bitcoins": BITCOINS_EXAMEN,
        "preguntas": [
            # Desigualdades lineales, cuadráticas, racionales y compuestas
            {"texto": "Resuelve: 2x + 3 > 7. ¿Cuál es la solución?",
             "opciones": ["x > 2", "x < 2", "x > 5"], "respuesta": "x > 2"},
            {"texto": "¿Para qué valores de x es cierto que x² − 4 < 0?",
             "opciones": ["−2 < x < 2", "x > 2", "x < −2"], "respuesta": "−2 < x < 2"},
            {"texto": "En la desigualdad (x − 1)/(x + 2) ≥ 0, ¿qué valor de x no puede estar en el dominio?",
             "opciones": ["x = −2", "x = 1", "x = 0"], "respuesta": "x = −2"},
            {"texto": "¿Qué describe la desigualdad compuesta −2 < x ≤ 5?",
             "opciones": ["x está entre −2 (sin incluir) y 5 (incluido)", "x es menor que −2 o mayor que 5", "x es exactamente −2 o 5"],
             "respuesta": "x está entre −2 (sin incluir) y 5 (incluido)"},
            {"texto": "¿Cuánto vale |−7| (valor absoluto)?", "opciones": ["7", "−7", "0"], "respuesta": "7"},
            # Ecuaciones cuadráticas y tiro parabólico
            {"texto": "La gráfica de una función cuadrática tiene forma de:",
             "opciones": ["Parábola", "Línea recta", "Círculo"], "respuesta": "Parábola"},
            {"texto": "Resuelve x² − 9 = 0. ¿Cuáles son sus soluciones?",
             "opciones": ["x = 3 y x = −3", "x = 9", "Solo x = 3"], "respuesta": "x = 3 y x = −3"},
            # Funciones: evaluación y gráficas
            {"texto": "Si f(x) = x² − 4, ¿cuánto vale f(3)?", "opciones": ["5", "9", "−5"], "respuesta": "5"},
            {"texto": "El dominio de una función es:",
             "opciones": ["El conjunto de valores de entrada (x) para los que está definida", "El conjunto de valores de salida (y)", "La pendiente de la función"],
             "respuesta": "El conjunto de valores de entrada (x) para los que está definida"},
            # Funciones: vocabulario y transformaciones
            {"texto": "Si f(−x) = f(x) para toda x, la función es:",
             "opciones": ["Par", "Impar", "Ninguna de las dos"], "respuesta": "Par"},
            {"texto": "(f ∘ g)(x) significa:",
             "opciones": ["f(g(x)): primero se evalúa g, luego f sobre ese resultado", "f(x) · g(x)", "f(x) + g(x)"],
             "respuesta": "f(g(x)): primero se evalúa g, luego f sobre ese resultado"},
            # Exponenciales, logaritmos y límites
            {"texto": "En f(x) = aˣ, ¿dónde está la variable?",
             "opciones": ["En el exponente", "En la base", "No aparece"], "respuesta": "En el exponente"},
            {"texto": "Según las leyes de los logaritmos, log(a·b) es igual a:",
             "opciones": ["log(a) + log(b)", "log(a) · log(b)", "log(a) − log(b)"], "respuesta": "log(a) + log(b)"},
            {"texto": "La expresión 0/0, al evaluar un límite directamente, se llama:",
             "opciones": ["Una indeterminación", "Una asíntota", "Un dominio"], "respuesta": "Una indeterminación"},
            # Derivación: regla de la cadena
            {"texto": "Para derivar f(g(x)), la regla de la cadena dice que la derivada es:",
             "opciones": ["f'(g(x)) · g'(x)", "f'(x) · g'(x)", "f(g'(x))"], "respuesta": "f'(g(x)) · g'(x)"},
        ],
    },
    "algebra": {
        "agente": "Agente ÁLGEBRA",
        "tiempo_limite": TIEMPO_LIMITE,
        "aciertos_minimos": ACIERTOS_MINIMOS,
        "bitcoins": BITCOINS_EXAMEN,
        "preguntas": [
            # Números reales y sistemas de ecuaciones
            {"texto": "¿Cuál de los siguientes es un número irracional?",
             "opciones": ["√2", "1/2", "4"], "respuesta": "√2"},
            {"texto": "La propiedad que dice que a + b = b + a se llama:",
             "opciones": ["Conmutativa", "Asociativa", "Distributiva"], "respuesta": "Conmutativa"},
            {"texto": "¿Cuál es el valor de x en el sistema x + y = 5, x − y = 1?",
             "opciones": ["x = 3", "x = 2", "x = 4"], "respuesta": "x = 3"},
            # Polinomios y teoremas fundamentales
            {"texto": "¿Cuál de las siguientes expresiones es un polinomio?",
             "opciones": ["3x² − 2x + 5", "3/x + 2", "√x + 1"], "respuesta": "3x² − 2x + 5"},
            {"texto": "Al dividir un polinomio P(x) entre otro, el resultado incluye un cociente y un:",
             "opciones": ["Residuo", "Exponente", "Coeficiente"], "respuesta": "Residuo"},
            {"texto": "Según el teorema del residuo, al dividir P(x) entre (x − a), el residuo es igual a:",
             "opciones": ["P(a)", "P(0)", "P(x)/a"], "respuesta": "P(a)"},
            {"texto": "(x − a) es un factor de P(x) si y solo si:",
             "opciones": ["P(a) = 0", "P(a) = 1", "a = 0"], "respuesta": "P(a) = 0"},
            # Naturaleza de las raíces
            {"texto": "Una raíz racional de una ecuación puede escribirse como:",
             "opciones": ["Una fracción de dos enteros", "Un número con parte imaginaria", "Un número irracional"],
             "respuesta": "Una fracción de dos enteros"},
            {"texto": "Las raíces complejas de un polinomio con coeficientes reales siempre aparecen:",
             "opciones": ["En pares conjugados", "Solas", "Nunca"], "respuesta": "En pares conjugados"},
            # Análisis y acotación de raíces
            {"texto": "La regla de los signos de Descartes se usa para:",
             "opciones": ["Acotar cuántas raíces reales positivas o negativas tiene un polinomio", "Resolver sistemas de ecuaciones", "Sumar matrices"],
             "respuesta": "Acotar cuántas raíces reales positivas o negativas tiene un polinomio"},
            # Álgebra matricial y operaciones con matrices
            {"texto": "Una matriz es:",
             "opciones": ["Un arreglo rectangular de números en filas y columnas", "Una ecuación con una incógnita", "Un tipo de función"],
             "respuesta": "Un arreglo rectangular de números en filas y columnas"},
            {"texto": "Una matriz con unos en la diagonal y ceros en el resto de sus posiciones se llama matriz:",
             "opciones": ["Identidad", "Nula", "Rectangular"], "respuesta": "Identidad"},
            {"texto": "¿Cuándo se pueden sumar dos matrices?",
             "opciones": ["Cuando tienen el mismo tamaño", "Siempre, sin importar su tamaño", "Nunca"],
             "respuesta": "Cuando tienen el mismo tamaño"},
            {"texto": "Para multiplicar dos matrices A · B, se requiere que:",
             "opciones": ["El número de columnas de A sea igual al número de filas de B", "Ambas sean matrices cuadradas", "Tengan exactamente el mismo tamaño"],
             "respuesta": "El número de columnas de A sea igual al número de filas de B"},
            {"texto": "La matriz inversa A⁻¹ cumple que A · A⁻¹ es igual a:",
             "opciones": ["La matriz identidad", "La matriz nula", "A misma"], "respuesta": "La matriz identidad"},
        ],
    },

    # CU15 (batalla final): todavía no desarrollado -usa retos reales en
    # modo avanzado, no preguntas de opción múltiple, ver la especificación
    # de CU15-, así que este bloque sigue siendo solo de ejemplo.
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
