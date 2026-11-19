"""
Relacionar conceptos (CU-13): alinear tres carretes giratorios (concepto,
palabra clave, definición) para formar combinaciones válidas, en 3 rondas
de 3, 4 y 5 combinaciones. El banco de combinaciones se configura por
materia (R62b) sin tocar la mecánica.

Cada carrete se mezcla con una semilla fija (independiente para cada
columna), así el orden siempre sale igual pero las tres columnas no quedan
alineadas por posición: el alumno tiene que girar cada una por separado
para encontrar la combinación correcta.
"""
import random

EJERCICIOS = {
    "logica-programacion": {
        "titulo": "Relacionar conceptos",
        "bitcoins": 30,
        "semilla": "logica-programacion",
        "rondas": [
            [
                {"concepto": "Variable", "palabra": "var", "definicion": "Guarda un valor para usarlo después."},
                {"concepto": "Bucle", "palabra": "for / while", "definicion": "Repite un bloque de código varias veces."},
                {"concepto": "Función", "palabra": "def", "definicion": "Agrupa código para reutilizarlo."},
            ],
            [
                {"concepto": "Condicional", "palabra": "if / else", "definicion": "Ejecuta código según una condición."},
                {"concepto": "Arreglo", "palabra": "lista", "definicion": "Almacena varios elementos ordenados."},
                {"concepto": "Clase", "palabra": "class", "definicion": "Plantilla para crear objetos con datos y comportamiento."},
                {"concepto": "Constante", "palabra": "const", "definicion": "Valor que no cambia una vez asignado."},
            ],
            [
                {"concepto": "Recursión", "palabra": "llamada a sí misma", "definicion": "Una función que se invoca a sí misma para resolver un problema."},
                {"concepto": "Excepción", "palabra": "try / except", "definicion": "Manejo de errores que ocurren durante la ejecución."},
                {"concepto": "Comentario", "palabra": "#", "definicion": "Texto que el programa ignora, para explicar el código."},
                {"concepto": "Parámetro", "palabra": "argumento", "definicion": "Valor que se le pasa a una función al llamarla."},
                {"concepto": "Booleano", "palabra": "True / False", "definicion": "Tipo de dato con solo dos valores posibles."},
            ],
        ],
    },
    # Introprog · Fundamentos de computación y herramientas (Módulo 0 del temario).
    "fundamentos-computacion": {
        "titulo": "Relacionar conceptos: fundamentos",
        "bitcoins": 30,
        "semilla": "fundamentos-computacion",
        "rondas": [
            [
                {"concepto": "Paradigma imperativo", "palabra": "paso a paso", "definicion": "Instrucciones que van modificando el estado del programa en orden."},
                {"concepto": "Paradigma declarativo", "palabra": "qué, no cómo", "definicion": "Se especifica el resultado que se busca sin detallar los pasos para lograrlo."},
                {"concepto": "Programación orientada a objetos", "palabra": "POO", "definicion": "Organiza el código alrededor de objetos que combinan datos y comportamiento."},
            ],
            [
                {"concepto": "Editor de texto", "palabra": "escribir código", "definicion": "Programa donde se escribe el código fuente, sin ejecutarlo ni revisarlo."},
                {"concepto": "IDE", "palabra": "entorno integrado", "definicion": "Editor, depurador y herramientas juntos en un solo programa."},
                {"concepto": "Compilador", "palabra": "traduce todo junto", "definicion": "Convierte el código fuente completo en un programa ejecutable antes de correrlo."},
                {"concepto": "Intérprete", "palabra": "ejecuta línea por línea", "definicion": "Lee y ejecuta el código una instrucción a la vez, sin generar un ejecutable aparte."},
            ],
            [
                {"concepto": "Paradigma funcional", "palabra": "funciones puras", "definicion": "Basado en evaluar funciones matemáticas puras y datos que no cambian."},
                {"concepto": "Paradigma reactivo", "palabra": "flujos de datos", "definicion": "Orientado a flujos de datos asíncronos y propagación automática de cambios."},
                {"concepto": "Paradigma lógico", "palabra": "reglas y hechos", "definicion": "Basado en reglas formales, hechos e inferencia lógica."},
                {"concepto": "Algoritmo", "palabra": "serie de pasos", "definicion": "Conjunto finito y preciso de pasos para resolver un problema."},
                {"concepto": "Pseudocódigo", "palabra": "casi lenguaje humano", "definicion": "Forma de escribir un algoritmo con palabras parecidas al lenguaje natural, sin sintaxis estricta."},
            ],
        ],
    },
    # Introprog · Introducción a POO (Módulo 5 del temario).
    "poo-pilares": {
        "titulo": "Relacionar conceptos: POO",
        "bitcoins": 30,
        "semilla": "poo-pilares",
        "rondas": [
            [
                {"concepto": "Clase", "palabra": "molde", "definicion": "Definición o plantilla a partir de la cual se crean objetos."},
                {"concepto": "Objeto", "palabra": "instancia", "definicion": "Ejemplar concreto creado a partir de una clase, con sus propios datos."},
                {"concepto": "Atributo", "palabra": "dato del objeto", "definicion": "Característica o dato que guarda un objeto."},
            ],
            [
                {"concepto": "Método", "palabra": "comportamiento", "definicion": "Función definida dentro de una clase que describe lo que un objeto puede hacer."},
                {"concepto": "Constructor", "palabra": "__init__", "definicion": "Método especial que inicializa el estado de un objeto al crearse."},
                {"concepto": "Encapsulación", "palabra": "protección de datos", "definicion": "Control del acceso a los datos internos de un objeto."},
                {"concepto": "Herencia", "palabra": "clase padre e hija", "definicion": "Una clase reutiliza y especializa atributos y métodos de otra."},
            ],
            [
                {"concepto": "Polimorfismo", "palabra": "misma interfaz, distinta forma", "definicion": "Distintos objetos responden a su manera a un mismo método."},
                {"concepto": "Composición", "palabra": "tiene un", "definicion": "Una clase se construye integrando instancias de otras clases."},
                {"concepto": "Análisis semántico", "palabra": "sustantivos y verbos", "definicion": "Identificar posibles clases (sustantivos) y métodos (verbos) en un enunciado."},
                {"concepto": "Instancia", "palabra": "objeto creado", "definicion": "Un objeto particular creado a partir de una clase."},
                {"concepto": "Estado", "palabra": "datos actuales", "definicion": "El conjunto de valores que tienen los atributos de un objeto en un momento dado."},
            ],
        ],
    },
    # Cálculo · Desigualdades racionales (Módulo 1 del temario).
    "desigualdades-racionales": {
        "titulo": "Relacionar conceptos: desigualdades racionales",
        "bitcoins": 30,
        "semilla": "desigualdades-racionales",
        "rondas": [
            [
                {"concepto": "Denominador", "palabra": "no puede ser cero", "definicion": "La parte de abajo de la fracción; si vale 0 la expresión no está definida."},
                {"concepto": "Dominio restringido", "palabra": "excluye puntos", "definicion": "El conjunto de valores de x donde la desigualdad racional sí está definida."},
                {"concepto": "Asíntota vertical", "palabra": "línea que no se toca", "definicion": "Recta vertical donde el denominador se hace cero y la gráfica se dispara."},
            ],
            [
                {"concepto": "Punto crítico", "palabra": "cambia de signo", "definicion": "Valor de x donde el numerador o el denominador se vuelven cero."},
                {"concepto": "Tabla de signos", "palabra": "organiza el análisis", "definicion": "Método para ver en qué intervalos la expresión racional es positiva o negativa."},
                {"concepto": "Intervalo abierto", "palabra": "no incluye el extremo", "definicion": "Notación que excluye el valor exacto donde el denominador se anula."},
                {"concepto": "Numerador", "palabra": "la parte de arriba", "definicion": "La parte de la fracción que se divide entre el denominador."},
            ],
            [
                {"concepto": "Simplificación", "palabra": "factorizar primero", "definicion": "Reducir la expresión racional antes de analizar su signo."},
                {"concepto": "Signo del cociente", "palabra": "positivo o negativo", "definicion": "Depende de si numerador y denominador tienen el mismo signo o distinto."},
                {"concepto": "Valor no permitido", "palabra": "fuera del dominio", "definicion": "Un valor de x que haría cero al denominador y por eso se excluye siempre de la solución."},
                {"concepto": "Desigualdad estricta", "palabra": "> o <", "definicion": "No incluye los puntos donde la expresión vale exactamente cero o es indefinida."},
                {"concepto": "Desigualdad no estricta", "palabra": "≥ o ≤", "definicion": "Puede incluir el cero del numerador, pero nunca el del denominador."},
            ],
        ],
    },
    # Cálculo · Funciones, gráficas y operaciones (Módulo 2 del temario).
    "funciones-vocabulario": {
        "titulo": "Relacionar conceptos: funciones",
        "bitcoins": 30,
        "semilla": "funciones-vocabulario",
        "rondas": [
            [
                {"concepto": "Dominio", "palabra": "valores de x", "definicion": "Conjunto de todos los valores de entrada para los que la función está definida."},
                {"concepto": "Rango", "palabra": "valores de y", "definicion": "Conjunto de todos los valores de salida que produce la función."},
                {"concepto": "Función par", "palabra": "f(−x) = f(x)", "definicion": "Su gráfica es simétrica respecto al eje y."},
            ],
            [
                {"concepto": "Función impar", "palabra": "f(−x) = −f(x)", "definicion": "Su gráfica es simétrica respecto al origen."},
                {"concepto": "Asíntota", "palabra": "línea que no se cruza", "definicion": "Recta a la que la gráfica de la función se acerca sin tocarla."},
                {"concepto": "Composición", "palabra": "f∘g", "definicion": "Aplicar primero g y después f al resultado: f(g(x))."},
                {"concepto": "Función inversa", "palabra": "f⁻¹", "definicion": "Función que deshace lo que hace f, intercambiando entradas y salidas."},
            ],
            [
                {"concepto": "Reflexión", "palabra": "espejo", "definicion": "Transformación que voltea la gráfica respecto a un eje."},
                {"concepto": "Desplazamiento vertical", "palabra": "sube o baja", "definicion": "Sumar o restar una constante a f(x) mueve la gráfica hacia arriba o abajo."},
                {"concepto": "Desplazamiento horizontal", "palabra": "izquierda o derecha", "definicion": "Sumar o restar dentro del argumento mueve la gráfica a los lados."},
                {"concepto": "Estiramiento", "palabra": "más alto o más ancho", "definicion": "Multiplicar f(x) o su entrada por una constante cambia qué tan \"apretada\" se ve la gráfica."},
                {"concepto": "Intersección con los ejes", "palabra": "dónde cruza", "definicion": "Puntos donde la gráfica toca el eje x (raíces) o el eje y."},
            ],
        ],
    },
    # Linux · Lectura de archivos y bitácoras (Módulo 3a del temario).
    "lectura-bitacoras": {
        "titulo": "Relacionar conceptos: lectura de archivos",
        "bitcoins": 30,
        "semilla": "lectura-bitacoras",
        "rondas": [
            [
                {"concepto": "cat", "palabra": "mostrar completo", "definicion": "Muestra todo el contenido del archivo de una vez."},
                {"concepto": "less", "palabra": "paginado", "definicion": "Muestra el archivo página por página para navegarlo con calma."},
                {"concepto": "nano", "palabra": "editor", "definicion": "Editor de texto sencillo para crear o modificar archivos en la terminal."},
            ],
            [
                {"concepto": "head", "palabra": "primeras líneas", "definicion": "Muestra el inicio de un archivo."},
                {"concepto": "tail", "palabra": "últimas líneas", "definicion": "Muestra el final de un archivo."},
                {"concepto": "bitácora", "palabra": "log", "definicion": "Registro cronológico de eventos que genera un sistema o programa."},
                {"concepto": "texto plano", "palabra": "sin formato", "definicion": "Archivo que solo contiene caracteres, sin estilos ni formato especial."},
            ],
            [
                {"concepto": "Ctrl+O", "palabra": "guardar", "definicion": "Atajo de nano para guardar los cambios en el archivo."},
                {"concepto": "Ctrl+X", "palabra": "salir", "definicion": "Atajo de nano para cerrar el editor."},
                {"concepto": "wc -l", "palabra": "contar líneas", "definicion": "Cuenta cuántas líneas tiene un archivo."},
                {"concepto": "log rotado", "palabra": "archivo histórico", "definicion": "Bitácora anterior que el sistema guarda aparte cuando la actual crece mucho."},
                {"concepto": "timestamp", "palabra": "marca de tiempo", "definicion": "Fecha y hora que acompaña cada línea de una bitácora."},
            ],
        ],
    },
}


def total_rondas(ejercicio):
    return len(ejercicio["rondas"])


def _mezclar(lista, semilla):
    azar = random.Random(semilla)
    copia = list(lista)
    azar.shuffle(copia)
    return copia


def datos_publicos(ejercicio):
    """Las tres columnas de cada ronda, mezcladas de forma independiente
    (misma semilla siempre, para que el reto salga igual). Nunca se manda
    qué índice de cada columna forma una combinación válida."""
    rondas = []
    for numero, combos in enumerate(ejercicio["rondas"]):
        base = f"{ejercicio['semilla']}-{numero}"
        rondas.append({
            "conceptos": _mezclar([c["concepto"] for c in combos], base + "-concepto"),
            "palabras": _mezclar([c["palabra"] for c in combos], base + "-palabra"),
            "definiciones": _mezclar([c["definicion"] for c in combos], base + "-definicion"),
            "total": len(combos),
        })
    return {"rondas": rondas, "total_rondas": len(rondas)}


def verificar_combinacion(ejercicio, numero_ronda, concepto, palabra, definicion):
    """True si (concepto, palabra, definicion) es una de las combinaciones
    válidas de esa ronda (sin importar en qué posición de carrete esté)."""
    if not (0 <= numero_ronda < len(ejercicio["rondas"])):
        return False
    return any(
        combo["concepto"] == concepto and combo["palabra"] == palabra and combo["definicion"] == definicion
        for combo in ejercicio["rondas"][numero_ronda]
    )
