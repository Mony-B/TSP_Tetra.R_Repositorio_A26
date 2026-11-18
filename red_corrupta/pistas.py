"""
Catálogo de pistas de la red corrupta (CU03).

Una pista es la definición de UN concepto del temario (ver
TSP_Tetra.R_Temario_A26_1.pdf), nunca una pregunta con respuesta: el
alumno no "contesta" nada aquí, solo la desbloquea (comprándola con 10
bitcoins o superando Snake) y la consulta. Por eso, a diferencia de los
EJERCICIOS de cada app de reto, esto no son preguntas ni respuestas
correctas/incorrectas.

El catálogo cubre las 5 materias que sí tienen retos (Lógica y
algoritmos, Introducción a la programación, Linux, Cálculo, Álgebra).
Ética e IA queda fuera a propósito: el temario la marca como "Eje
integrado a la narrativa del guion, sin reto", así que no hay ningún
reto al que una pista de esa materia pudiera ayudar.

Las pistas NO se guardan en la base de datos (igual que EJERCICIOS en
cada app de reto): solo se guarda, por alumno, cuáles ya desbloqueó
(ver progreso.models.PistaAdquirida). El identificador de cada pista
("materia:subtema:concepto") es justo lo que se guarda en el campo
`pista` de esa tabla.

Estructura:

CATALOGO = {
    "<slug_materia>": {
        "nombre": "<nombre de la materia>",
        "subtemas": {
            "<slug_subtema>": {
                "nombre": "<nombre del subtema>",
                "pistas": [
                    {"slug": "...", "termino": "...", "definicion": "..."},
                    ...
                ],
            },
            ...
        },
    },
    ...
}

`pista_id()` arma el identificador completo; `todas_las_pistas()` y
`PISTAS` (índice plano por id) son lo que usa el resto de la app.
"""


def _p(slug, termino, definicion):
    return {"slug": slug, "termino": termino, "definicion": definicion}


CATALOGO = {
    # ------------------------------------------------------------------
    "logica": {
        "nombre": "Lógica y algoritmos",
        "subtemas": {
            "conjuntos-venn": {
                "nombre": "Conjuntos y diagramas de Venn",
                "pistas": [
                    _p("conjunto", "Conjunto",
                       "Colección de elementos distintos, sin orden ni repetición, que comparten "
                       "o no una propiedad. Puede ser finito, infinito, vacío (∅, sin elementos) "
                       "o unitario (un solo elemento)."),
                    _p("tipos-de-conjuntos", "Tipos de conjuntos",
                       "Clasificación según su contenido: vacío (sin elementos), unitario (un "
                       "elemento), finito (número contable de elementos), infinito (no contable) "
                       "y universo (todos los elementos posibles en el contexto del problema)."),
                    _p("union", "Unión (∪)",
                       "Operación entre dos conjuntos A y B que da como resultado un conjunto con "
                       "todos los elementos que están en A, en B, o en ambos. A ∪ B = {x | x ∈ A o x ∈ B}."),
                    _p("interseccion", "Intersección (∩)",
                       "Operación entre dos conjuntos A y B que da como resultado solo los "
                       "elementos que están en ambos a la vez. A ∩ B = {x | x ∈ A y x ∈ B}."),
                    _p("diferencia", "Diferencia (−)",
                       "Operación A − B que da los elementos que están en A pero no en B. No es "
                       "conmutativa: A − B casi siempre es distinto de B − A."),
                    _p("complemento", "Complemento (A′ o Aᶜ)",
                       "Todos los elementos del conjunto universo que NO pertenecen a A. "
                       "Equivale a Universo − A."),
                    _p("pertenencia", "Pertenencia (∈)",
                       "Relación entre un elemento y un conjunto: x ∈ A significa que x es uno de "
                       "los elementos de A. x ∉ A significa que no lo es."),
                    _p("inclusion", "Inclusión (⊆)",
                       "Relación entre dos conjuntos: A ⊆ B significa que todo elemento de A "
                       "también está en B (A es subconjunto de B). Si además A ≠ B, se llama "
                       "subconjunto propio (A ⊂ B)."),
                    _p("diagrama-de-venn", "Diagrama de Venn",
                       "Representación gráfica de conjuntos como círculos superpuestos dentro de "
                       "un rectángulo (el universo), donde las zonas de traslape muestran "
                       "visualmente uniones, intersecciones y diferencias."),
                ],
            },
            "logica-proposicional": {
                "nombre": "Lógica proposicional y tablas de verdad",
                "pistas": [
                    _p("proposicion", "Proposición",
                       "Enunciado que puede calificarse como verdadero o falso, pero no ambos a "
                       "la vez. \"5 es mayor que 3\" es una proposición; \"¿qué hora es?\" no lo es."),
                    _p("conjuncion-and", "Conjunción (AND, ∧)",
                       "Conector lógico que une dos proposiciones y es verdadero solo cuando "
                       "ambas son verdaderas. p ∧ q."),
                    _p("disyuncion-or", "Disyunción (OR, ∨)",
                       "Conector lógico que une dos proposiciones y es verdadero cuando al menos "
                       "una de las dos es verdadera. p ∨ q."),
                    _p("negacion-not", "Negación (NOT, ¬)",
                       "Conector que invierte el valor de verdad de una proposición: si p es "
                       "verdadero, ¬p es falso, y viceversa."),
                    _p("condicional", "Condicional (→)",
                       "Conector \"si p, entonces q\" (p → q). Es falso únicamente cuando p es "
                       "verdadero y q es falso; en cualquier otro caso es verdadero."),
                    _p("bicondicional", "Bicondicional (↔)",
                       "Conector \"p si y solo si q\" (p ↔ q). Es verdadero cuando p y q tienen "
                       "el mismo valor de verdad (ambas verdaderas o ambas falsas)."),
                    _p("tabla-de-verdad", "Tabla de verdad",
                       "Tabla que enumera todas las combinaciones posibles de valores de verdad "
                       "de las proposiciones involucradas y el resultado de una expresión lógica "
                       "para cada combinación."),
                    _p("puertas-logicas", "Puertas lógicas",
                       "Componentes electrónicos que implementan los conectores lógicos (AND, OR, "
                       "NOT, y derivadas como NAND, NOR, XOR) para construir circuitos digitales."),
                ],
            },
            "algebra-proposiciones": {
                "nombre": "Álgebra de proposiciones y demostración",
                "pistas": [
                    _p("de-morgan", "Leyes de De Morgan",
                       "¬(p ∧ q) equivale a (¬p ∨ ¬q), y ¬(p ∨ q) equivale a (¬p ∧ ¬q): negar una "
                       "conjunción/disyunción se vuelve la disyunción/conjunción de las "
                       "negaciones."),
                    _p("simplificacion-proposicional", "Simplificación de proposiciones",
                       "Uso de leyes lógicas (De Morgan, distributiva, absorción, idempotencia, "
                       "entre otras) para reescribir una expresión lógica de forma más corta sin "
                       "cambiar su valor de verdad."),
                    _p("fnd", "Forma normal disyuntiva (FND)",
                       "Expresión lógica escrita como una disyunción (OR) de conjunciones (AND) "
                       "de literales, por ejemplo (p ∧ q) ∨ (¬p ∧ r)."),
                    _p("fnc", "Forma normal conjuntiva (FNC)",
                       "Expresión lógica escrita como una conjunción (AND) de disyunciones (OR) "
                       "de literales, por ejemplo (p ∨ q) ∧ (¬p ∨ r)."),
                    _p("contrapositiva", "Demostración por contrapositiva",
                       "Para probar \"si p entonces q\", en vez se prueba su contrapositiva "
                       "\"si no q entonces no p\", que es lógicamente equivalente y a veces más "
                       "fácil de demostrar."),
                    _p("induccion", "Demostración por inducción",
                       "Técnica para probar que una propiedad se cumple para todos los números "
                       "naturales: se prueba el caso base (normalmente n=0 o n=1) y luego que, si "
                       "se cumple para n, también se cumple para n+1."),
                    _p("recursion", "Recursión",
                       "Técnica en la que una función o definición se refiere a sí misma para "
                       "resolver un problema, dividiéndolo en casos más pequeños hasta llegar a "
                       "un caso base que no vuelve a llamarse."),
                    _p("complejidad", "Complejidad (computacional)",
                       "Medida de cuántos recursos (normalmente tiempo) necesita un algoritmo en "
                       "función del tamaño de la entrada, expresada con notación como O(n) o "
                       "O(n²)."),
                ],
            },
        },
    },
    # ------------------------------------------------------------------
    "introprog": {
        "nombre": "Introducción a la programación",
        "subtemas": {
            "fundamentos-paradigmas": {
                "nombre": "Fundamentos y paradigmas",
                "pistas": [
                    _p("algoritmo", "Algoritmo",
                       "Secuencia finita y ordenada de pasos precisos que resuelve un problema o "
                       "realiza una tarea, sin ambigüedad en ninguno de sus pasos."),
                    _p("paradigma-imperativo", "Paradigma imperativo",
                       "Estilo de programación que describe el cómo: una secuencia de "
                       "instrucciones que cambian el estado del programa paso a paso (ej. "
                       "asignaciones, ciclos)."),
                    _p("paradigma-poo", "Paradigma orientado a objetos (POO)",
                       "Estilo de programación que organiza el código en objetos, que combinan "
                       "datos (atributos) y comportamiento (métodos) relacionados entre sí."),
                    _p("paradigma-funcional", "Paradigma funcional",
                       "Estilo de programación que trata la computación como la evaluación de "
                       "funciones matemáticas, evitando cambiar estado y usando funciones puras."),
                    _p("editor-de-texto", "Editor (de código)",
                       "Programa para escribir y modificar código fuente como texto plano, con "
                       "ayudas como resaltado de sintaxis."),
                    _p("ide", "IDE",
                       "Entorno de Desarrollo Integrado: programa que junta editor, compilador o "
                       "intérprete, depurador y otras herramientas en una sola aplicación."),
                    _p("compilador", "Compilador",
                       "Programa que traduce todo el código fuente a código máquina (o a otro "
                       "lenguaje) antes de ejecutarlo, generando un archivo ejecutable aparte."),
                    _p("interprete", "Intérprete",
                       "Programa que lee y ejecuta el código fuente línea por línea, sin generar "
                       "antes un archivo ejecutable independiente (así funciona Python)."),
                ],
            },
            "python-basico": {
                "nombre": "Python básico: datos y sentencias",
                "pistas": [
                    _p("hola-mundo", "\"Hola Mundo\"",
                       "El programa más simple posible en un lenguaje, que solo muestra un "
                       "mensaje de texto; se usa tradicionalmente para probar que el entorno de "
                       "desarrollo funciona."),
                    _p("variable", "Variable",
                       "Espacio con nombre que guarda un valor en memoria y que se puede leer o "
                       "modificar durante la ejecución del programa."),
                    _p("tipos-de-datos", "Tipos de datos",
                       "Categorías que indica qué clase de valor guarda una variable y qué "
                       "operaciones admite: por ejemplo int (enteros), float (decimales), str "
                       "(texto) y bool (verdadero/falso)."),
                    _p("operadores", "Operadores",
                       "Símbolos que realizan una operación sobre uno o más valores: aritméticos "
                       "(+, -, *, /), de comparación (==, <, >) y lógicos (and, or, not), entre "
                       "otros."),
                    _p("input", "input()",
                       "Función de Python que pausa el programa y espera a que el usuario escriba "
                       "algo en la terminal, devolviéndolo como texto (str)."),
                    _p("print", "print()",
                       "Función de Python que muestra uno o más valores en la terminal como "
                       "salida del programa."),
                ],
            },
            "control-de-flujo": {
                "nombre": "Control de flujo: condicionales y ciclos",
                "pistas": [
                    _p("condicional-if-elif-else", "if / elif / else",
                       "Estructura que ejecuta un bloque de código distinto según si una "
                       "condición es verdadera (if), otra condición alterna (elif) o ninguna de "
                       "las anteriores (else)."),
                    _p("ciclo-while", "Ciclo while",
                       "Repite un bloque de código mientras una condición siga siendo "
                       "verdadera; se evalúa la condición antes de cada repetición."),
                    _p("ciclo-for", "Ciclo for",
                       "Repite un bloque de código una vez por cada elemento de una secuencia "
                       "(como un rango de números o una lista)."),
                    _p("arreglo", "Arreglo (lista)",
                       "Estructura que guarda varios valores en un orden fijo, accesibles cada "
                       "uno por su posición (índice)."),
                    _p("indexacion-desde-cero", "Indexación desde 0",
                       "Convención en la que el primer elemento de un arreglo o secuencia tiene "
                       "índice 0, el segundo índice 1, y así sucesivamente."),
                ],
            },
            "subrutinas-funciones": {
                "nombre": "Subrutinas y funciones",
                "pistas": [
                    _p("procedimiento-vs-funcion", "Procedimiento vs. función",
                       "Un procedimiento ejecuta una serie de instrucciones sin regresar ningún "
                       "valor; una función ejecuta instrucciones y sí regresa un valor al código "
                       "que la llamó."),
                    _p("parametro", "Parámetro",
                       "Variable declarada entre los paréntesis de una función, que recibe un "
                       "valor (argumento) cada vez que la función se llama."),
                    _p("scope", "Scope (ámbito)",
                       "Región del código donde una variable existe y puede usarse. Una variable "
                       "definida dentro de una función normalmente no es visible fuera de ella "
                       "(ámbito local vs. global)."),
                ],
            },
            "introduccion-poo": {
                "nombre": "Introducción a POO",
                "pistas": [
                    _p("clase", "Clase",
                       "Plantilla o molde que define qué atributos y métodos tendrán los objetos "
                       "creados a partir de ella."),
                    _p("objeto", "Objeto",
                       "Instancia concreta de una clase, con sus propios valores para los "
                       "atributos definidos en esa clase."),
                    _p("atributo", "Atributo",
                       "Variable que pertenece a una clase (o a sus objetos) y guarda parte de su "
                       "estado o datos."),
                    _p("metodo", "Método",
                       "Función definida dentro de una clase que describe un comportamiento de "
                       "sus objetos; normalmente puede leer o modificar los atributos del objeto."),
                    _p("constructor", "Constructor",
                       "Método especial que se ejecuta automáticamente al crear un objeto nuevo, "
                       "usado para inicializar sus atributos (en Python, __init__)."),
                    _p("encapsulacion", "Encapsulación",
                       "Principio de POO que agrupa datos y comportamiento dentro de una clase y "
                       "oculta los detalles internos, exponiendo solo lo necesario hacia afuera."),
                    _p("herencia", "Herencia",
                       "Mecanismo por el que una clase (subclase) toma los atributos y métodos de "
                       "otra clase (superclase) y puede añadir o modificar los propios."),
                    _p("polimorfismo", "Polimorfismo",
                       "Capacidad de que objetos de distintas clases respondan de forma distinta "
                       "a un mismo método o mensaje, cada uno según su propia implementación."),
                    _p("composicion", "Composición",
                       "Relación en la que un objeto contiene a otros objetos como parte de sus "
                       "atributos, en vez de heredar de ellos (\"tiene un\" en vez de \"es un\")."),
                ],
            },
        },
    },
    # ------------------------------------------------------------------
    "linux": {
        "nombre": "Linux",
        "subtemas": {
            "terminal-fundamentos": {
                "nombre": "Terminal y fundamentos",
                "pistas": [
                    _p("kernel", "Kernel",
                       "Núcleo del sistema operativo: el programa que gestiona directamente el "
                       "hardware (procesador, memoria, dispositivos) y da servicio al resto del "
                       "software."),
                    _p("prompt", "Prompt",
                       "Línea de la terminal que indica que está lista para recibir un comando, "
                       "normalmente mostrando el usuario, el equipo y la carpeta actual."),
                    _p("whoami", "whoami",
                       "Comando que muestra el nombre del usuario con el que se inició sesión en "
                       "la terminal."),
                    _p("pwd", "pwd",
                       "Comando que muestra la ruta completa (absoluta) de la carpeta en la que "
                       "te encuentras actualmente (print working directory)."),
                    _p("clear", "clear",
                       "Comando que limpia la pantalla de la terminal, sin afectar el historial "
                       "de comandos."),
                    _p("echo", "echo",
                       "Comando que imprime en la terminal el texto que se le pasa como "
                       "argumento."),
                    _p("help", "help / --help",
                       "Comando o modificador que muestra información de uso y las opciones "
                       "disponibles de otro comando."),
                ],
            },
            "rutas-exploracion": {
                "nombre": "Rutas y exploración",
                "pistas": [
                    _p("ruta-absoluta", "Ruta absoluta",
                       "Ubicación de un archivo o carpeta descrita desde la raíz del sistema de "
                       "archivos (/), sin importar en qué carpeta estés parado. Ej.: /home/alumno/tarea.txt."),
                    _p("ruta-relativa", "Ruta relativa",
                       "Ubicación de un archivo o carpeta descrita a partir de la carpeta actual, "
                       "usando nombres de subcarpetas, \".\" (carpeta actual) o \"..\" (carpeta "
                       "anterior)."),
                    _p("cd", "cd",
                       "Comando para cambiar de carpeta actual en la terminal (change directory)."),
                    _p("ls", "ls",
                       "Comando que lista los archivos y carpetas dentro de la carpeta actual (o "
                       "de la que se le indique)."),
                ],
            },
            "gestion-archivos": {
                "nombre": "Gestión de archivos y carpetas",
                "pistas": [
                    _p("mkdir", "mkdir",
                       "Comando que crea una carpeta nueva (make directory)."),
                    _p("touch", "touch",
                       "Comando que crea un archivo vacío nuevo, o actualiza la fecha de "
                       "modificación de uno existente."),
                    _p("cp", "cp",
                       "Comando que copia un archivo o carpeta a otra ubicación, dejando el "
                       "original intacto (copy)."),
                    _p("mv", "mv",
                       "Comando que mueve o renombra un archivo o carpeta (move)."),
                    _p("rm", "rm",
                       "Comando que elimina un archivo; con la opción -r también elimina carpetas "
                       "completas (remove)."),
                ],
            },
            "lectura-busqueda": {
                "nombre": "Lectura, logs y búsqueda",
                "pistas": [
                    _p("cat", "cat",
                       "Comando que muestra todo el contenido de uno o varios archivos de texto "
                       "en la terminal, de corrido (concatenate)."),
                    _p("less", "less",
                       "Comando que muestra el contenido de un archivo de texto página por "
                       "página, permitiendo desplazarse hacia adelante y hacia atrás."),
                    _p("head", "head",
                       "Comando que muestra solo las primeras líneas de un archivo (10 por "
                       "defecto)."),
                    _p("tail", "tail",
                       "Comando que muestra solo las últimas líneas de un archivo (10 por "
                       "defecto); con -f sigue mostrando nuevas líneas en tiempo real (útil para "
                       "logs)."),
                    _p("nano", "nano",
                       "Editor de texto sencillo que corre dentro de la terminal, con atajos "
                       "visibles en la parte inferior de la pantalla."),
                    _p("find", "find",
                       "Comando que busca archivos y carpetas dentro de un árbol de directorios "
                       "según criterios como nombre, tipo o fecha."),
                    _p("grep", "grep",
                       "Comando que busca líneas que coincidan con un patrón de texto dentro de "
                       "uno o varios archivos."),
                    _p("tuberias", "Tuberías (|)",
                       "Operador que conecta la salida de un comando con la entrada de otro, "
                       "permitiendo encadenar comandos (ej. cat archivo.txt | grep error)."),
                ],
            },
            "permisos-procesos": {
                "nombre": "Permisos y procesos",
                "pistas": [
                    _p("ls-l", "ls -l",
                       "Variante de ls que muestra el listado en formato largo: permisos, dueño, "
                       "grupo, tamaño y fecha de modificación de cada archivo."),
                    _p("chmod", "chmod",
                       "Comando que cambia los permisos (lectura, escritura, ejecución) de un "
                       "archivo o carpeta, para el dueño, el grupo y los demás usuarios (change "
                       "mode)."),
                    _p("ps", "ps",
                       "Comando que muestra los procesos que están corriendo actualmente en el "
                       "sistema."),
                    _p("df-h", "df -h",
                       "Comando que muestra el espacio usado y disponible en los sistemas de "
                       "archivos montados, en un formato legible para humanos (-h)."),
                    _p("ctrl-c", "Ctrl+C",
                       "Combinación de teclas que envía una señal de interrupción al proceso que "
                       "está corriendo en primer plano en la terminal, deteniéndolo."),
                ],
            },
        },
    },
    # ------------------------------------------------------------------
    "calculo": {
        "nombre": "Cálculo",
        "subtemas": {
            "desigualdades-valor-absoluto": {
                "nombre": "Desigualdades, valor absoluto y tiro parabólico",
                "pistas": [
                    _p("desigualdad-lineal", "Desigualdad lineal",
                       "Desigualdad en la que la incógnita aparece solo elevada a la potencia 1, "
                       "como 2x + 3 > 7; su solución es un intervalo de números."),
                    _p("desigualdad-cuadratica", "Desigualdad cuadrática",
                       "Desigualdad en la que la incógnita aparece elevada al cuadrado, como "
                       "x² − 4 < 0; se resuelve analizando el signo de la expresión entre sus "
                       "raíces."),
                    _p("desigualdad-racional", "Desigualdad racional",
                       "Desigualdad en la que la incógnita aparece en el denominador de una "
                       "fracción; hay que excluir del dominio los valores que hacen cero al "
                       "denominador."),
                    _p("desigualdad-compuesta", "Desigualdad compuesta",
                       "Combinación de dos o más desigualdades unidas por \"y\" / \"o\" (unión o "
                       "intersección de sus soluciones), como −2 < x ≤ 5."),
                    _p("valor-absoluto", "Valor absoluto (|x|)",
                       "Distancia de un número a cero en la recta numérica, siempre positiva o "
                       "cero: |x| = x si x ≥ 0, y |x| = −x si x < 0."),
                    _p("parabola", "Parábola (tiro parabólico)",
                       "Curva que describe la trayectoria de un objeto lanzado bajo la gravedad; "
                       "es la gráfica de una función cuadrática, con forma de \"U\" (o \"U\" "
                       "invertida)."),
                ],
            },
            "funciones-transformaciones": {
                "nombre": "Funciones, gráficas y transformaciones",
                "pistas": [
                    _p("dominio", "Dominio",
                       "Conjunto de todos los valores de entrada (x) para los que una función "
                       "está definida."),
                    _p("rango", "Rango",
                       "Conjunto de todos los valores de salida (y) que una función realmente "
                       "produce."),
                    _p("desplazamiento-de-funciones", "Desplazamiento de funciones",
                       "Transformación que mueve la gráfica de una función hacia arriba/abajo "
                       "(sumando o restando una constante al resultado) o izquierda/derecha "
                       "(sumando o restando una constante a x)."),
                    _p("funcion-par-impar", "Función par / impar",
                       "Una función es par si f(−x) = f(x) (simétrica respecto al eje y); es "
                       "impar si f(−x) = −f(x) (simétrica respecto al origen)."),
                    _p("composicion-de-funciones", "Composición de funciones",
                       "Aplicar una función al resultado de otra: (f ∘ g)(x) = f(g(x)), primero "
                       "se evalúa g y luego f sobre ese resultado."),
                    _p("funcion-inversa", "Función inversa",
                       "Función f⁻¹ que \"deshace\" lo que hace f: si f(a) = b, entonces "
                       "f⁻¹(b) = a. Solo existe si f es biyectiva (uno a uno)."),
                ],
            },
            "exponenciales-logaritmos-limites": {
                "nombre": "Exponenciales, logaritmos y límites",
                "pistas": [
                    _p("exponencial", "Función exponencial",
                       "Función de la forma f(x) = aˣ (a > 0, a ≠ 1), donde la variable está en "
                       "el exponente; crece o decrece cada vez más rápido conforme x aumenta."),
                    _p("leyes-de-logaritmos", "Leyes de los logaritmos",
                       "Reglas para operar logaritmos: log(ab) = log(a) + log(b), "
                       "log(a/b) = log(a) − log(b), y log(aⁿ) = n·log(a)."),
                    _p("limite", "Límite",
                       "Valor al que se acerca una función f(x) conforme x se acerca a un punto "
                       "dado, sin que necesariamente f esté definida exactamente en ese punto."),
                    _p("indeterminacion", "Indeterminación",
                       "Expresión como 0/0 o ∞/∞ que, al evaluar un límite directamente, no da un "
                       "resultado claro y requiere técnicas adicionales (factorizar, racionalizar, "
                       "L'Hôpital) para resolverse."),
                    _p("asintota", "Asíntota",
                       "Recta a la que la gráfica de una función se acerca cada vez más sin "
                       "llegar a tocarla nunca (puede ser vertical, horizontal u oblicua)."),
                ],
            },
            "derivadas": {
                "nombre": "Derivadas y técnicas de derivación",
                "pistas": [
                    _p("derivada", "Derivada",
                       "Medida de qué tan rápido cambia una función en un punto: su pendiente "
                       "instantánea. Se escribe f′(x) o dy/dx."),
                    _p("reglas-basicas-derivacion", "Reglas básicas de derivación",
                       "Fórmulas directas para derivar: la derivada de una constante es 0, la de "
                       "xⁿ es n·xⁿ⁻¹ (regla de la potencia), y la derivada de una suma es la suma "
                       "de las derivadas."),
                    _p("regla-de-la-cadena", "Regla de la cadena",
                       "Para derivar una función compuesta f(g(x)), se multiplica la derivada de "
                       "f (evaluada en g(x)) por la derivada de g: (f∘g)′(x) = f′(g(x))·g′(x)."),
                    _p("derivacion-implicita", "Derivación implícita",
                       "Técnica para derivar una ecuación donde y no está despejada en términos "
                       "de x, derivando ambos lados respecto a x y tratando y como función de x."),
                    _p("derivacion-logaritmica", "Derivación logarítmica",
                       "Técnica que aplica logaritmo a ambos lados de una ecuación antes de "
                       "derivar, útil cuando la variable aparece tanto en la base como en el "
                       "exponente."),
                ],
            },
        },
    },
    # ------------------------------------------------------------------
    "algebra": {
        "nombre": "Álgebra",
        "subtemas": {
            "reales-sistemas-lineales": {
                "nombre": "Números reales y ecuaciones/sistemas lineales",
                "pistas": [
                    _p("numeros-reales", "Números reales",
                       "Conjunto que incluye a los naturales, enteros, racionales (fracciones) e "
                       "irracionales (como √2 o π); todo número que se puede ubicar en la recta "
                       "numérica."),
                    _p("propiedades-de-los-reales", "Propiedades de los reales",
                       "Reglas que cumplen las operaciones con números reales: conmutativa, "
                       "asociativa, distributiva, existencia de neutros (0 y 1) e inversos (aditivo "
                       "y multiplicativo)."),
                    _p("sistema-de-ecuaciones-lineales", "Sistema de ecuaciones lineales",
                       "Conjunto de dos o más ecuaciones lineales con las mismas incógnitas, que "
                       "se resuelven en conjunto buscando los valores que satisfacen a todas a la "
                       "vez (por sustitución, igualación o eliminación)."),
                ],
            },
            "polinomios-divisibilidad": {
                "nombre": "Polinomios y teoremas de divisibilidad",
                "pistas": [
                    _p("polinomio", "Polinomio",
                       "Expresión algebraica formada por la suma de términos, cada uno con una "
                       "variable elevada a una potencia entera no negativa multiplicada por un "
                       "coeficiente, como 3x² − 2x + 5."),
                    _p("multiplicacion-de-polinomios", "Multiplicación de polinomios",
                       "Multiplicar cada término de un polinomio por cada término del otro "
                       "(propiedad distributiva) y luego sumar los términos semejantes."),
                    _p("division-de-polinomios", "División de polinomios",
                       "Dividir un polinomio entre otro, obteniendo un cociente y un residuo, "
                       "normalmente usando división larga o división sintética."),
                    _p("teorema-del-residuo", "Teorema del residuo",
                       "Al dividir un polinomio P(x) entre (x − a), el residuo de esa división es "
                       "exactamente P(a)."),
                    _p("teorema-del-factor", "Teorema del factor",
                       "(x − a) es un factor de P(x) si y solo si P(a) = 0, es decir, si a es una "
                       "raíz del polinomio."),
                ],
            },
            "ecuaciones-raices": {
                "nombre": "Ecuaciones algebraicas y raíces",
                "pistas": [
                    _p("raiz-racional", "Raíz racional",
                       "Solución de una ecuación que puede escribirse como fracción de dos "
                       "enteros (p/q); el teorema de raíces racionales ayuda a listar los "
                       "candidatos posibles de un polinomio."),
                    _p("raiz-compleja", "Raíz compleja",
                       "Solución de una ecuación que incluye la unidad imaginaria i (donde "
                       "i² = −1), de la forma a + bi; en polinomios con coeficientes reales "
                       "siempre aparecen en pares conjugados."),
                    _p("raiz-irracional", "Raíz irracional",
                       "Solución de una ecuación que no puede escribirse como fracción exacta de "
                       "enteros, como √2 o (1 + √5)/2."),
                    _p("regla-de-descartes", "Regla de los signos de Descartes",
                       "Método que, contando los cambios de signo entre los coeficientes de un "
                       "polinomio, acota cuántas raíces reales positivas o negativas puede tener."),
                    _p("acotacion-de-raices", "Acotación de raíces",
                       "Técnicas para calcular un intervalo (una cota superior e inferior) donde "
                       "con seguridad se encuentran todas las raíces reales de un polinomio, antes "
                       "de buscarlas con precisión."),
                ],
            },
            "matrices": {
                "nombre": "Matrices y operaciones",
                "pistas": [
                    _p("matriz", "Matriz",
                       "Arreglo rectangular de números ordenados en filas y columnas, usado entre "
                       "otras cosas para representar sistemas de ecuaciones lineales."),
                    _p("tipos-de-matrices", "Tipos de matrices",
                       "Clasificación según su forma: cuadrada (mismas filas que columnas), "
                       "identidad (unos en la diagonal, ceros fuera), nula (todo ceros), diagonal, "
                       "entre otras."),
                    _p("suma-resta-de-matrices", "Suma y resta de matrices",
                       "Se suman o restan los elementos que están en la misma posición de ambas "
                       "matrices; solo se puede hacer entre matrices del mismo tamaño."),
                    _p("producto-de-matrices", "Producto de matrices",
                       "Multiplicación donde cada elemento del resultado es la suma de los "
                       "productos de una fila de la primera matriz por una columna de la segunda; "
                       "requiere que el número de columnas de la primera coincida con el número de "
                       "filas de la segunda."),
                    _p("matriz-inversa", "Matriz inversa",
                       "Matriz A⁻¹ que, multiplicada por la matriz original A, da la matriz "
                       "identidad (A · A⁻¹ = I). Solo existe si la matriz es cuadrada y su "
                       "determinante no es cero."),
                ],
            },
        },
    },
}


def pista_id(materia_slug, subtema_slug, pista_slug):
    return f"{materia_slug}:{subtema_slug}:{pista_slug}"


def todas_las_pistas():
    """Lista plana de todas las pistas del catálogo, cada una con su id
    completo y el nombre de su materia/subtema para mostrarlas agrupadas."""
    resultado = []
    for materia_slug, materia in CATALOGO.items():
        for subtema_slug, subtema in materia["subtemas"].items():
            for pista in subtema["pistas"]:
                resultado.append({
                    "id": pista_id(materia_slug, subtema_slug, pista["slug"]),
                    "materia_slug": materia_slug,
                    "materia": materia["nombre"],
                    "subtema_slug": subtema_slug,
                    "subtema": subtema["nombre"],
                    "termino": pista["termino"],
                    "definicion": pista["definicion"],
                })
    return resultado


# Índice plano {id: pista} para búsquedas directas (ver red_corrupta/views.py).
PISTAS = {p["id"]: p for p in todas_las_pistas()}
