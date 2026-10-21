"""
Comandos de Linux (CU-06): obtener la contraseña en una terminal.

El alumno explora un sistema de archivos SIMULADO con comandos de Linux. En
algún archivo está la contraseña (formato "PASSWORD: ...") y con ella abre la
puerta. Nada se ejecuta en el sistema real: cada comando lo interpreta
`ejecutar()` contra un diccionario que vive en la sesión del alumno.

Todo vive en el servidor: el navegador solo conoce el prompt inicial y recibe
la salida de cada comando. La contraseña nunca viaja hasta que el alumno la
encuentra.
"""
import fnmatch
import hmac
import re
import shlex
from copy import deepcopy

# Un archivo es un str; un directorio es un dict {nombre: contenido}.
# Los nombres que empiezan con "." están ocultos (solo se ven con `ls -a`).
#
# Cada NIVEL es un ejercicio completo con su propio sistema de archivos y su
# propia contraseña. Campos:
#   nivel, subtema, titulo, instrucciones, bitcoins
#   clave      - la contraseña de la puerta (en el archivo aparece como "PASSWORD: <clave>")
#   usuario    - quien es el alumno al empezar (lo muestra whoami)
#   comandos   - comandos habilitados en el nivel (los demás dan "Comando no encontrado")
#   sistema    - sistema de archivos inicial
#   solucion   - comandos que resuelven el nivel (solo para el equipo y las pruebas; no se manda al navegador)
# Campos opcionales:
#   disparadores - cuando se cumple "requiere" (rutas que deben existir como archivo) y
#       "ausentes" (rutas que ya no deben existir), aparece lo de "crea" ({ruta: contenido}).
#   usuarios / administradores / permisos - cuentas para `su` (valor = su clave, None si no
#       pide), cuentas que pueden usar chown y cambiar cualquier permiso, y dueño + modo octal
#       de ciertos archivos (ruta desde ~ -> {"dueno", "modo"}).
_LOG = "\n".join(
    [f"[INFO] 10:{i:02d} usuario{i % 7} inició sesión" for i in range(0, 20)]
    + ["[WARN] 10:20 PASSWORD: 12345 (intento fallido de usuario3)"]
    + [f"[INFO] 10:{i:02d} usuario{i % 5} cerró sesión" for i in range(21, 40)]
    + ["[ADMIN] 10:41 PASSWORD: gr3p_t4rg3t"]
    + [f"[INFO] 10:{i:02d} copia de seguridad {i} completada" for i in range(42, 55)]
)

NIVELES = {
    # Subtema 1 · Exploración del entorno: pwd, ls, ls -a, cd, whoami
    "basicos": {
        "nivel": 1,
        "subtema": "Exploración del entorno",
        "titulo": "La puerta cerrada",
        "instrucciones": (
            "Una puerta bloqueada te cierra el paso. Explora la terminal, "
            "encuentra la contraseña y escríbela en la puerta."
        ),
        "bitcoins": 50,
        "clave": "0cult0_4lumn0",
        "usuario": "alumno",
        "comandos": ["help", "clear", "pwd", "ls", "cd", "cat", "whoami"],
        "sistema": {
            "readme.txt": (
                "Bienvenido al sistema.\n"
                "La contraseña está en un archivo OCULTO cuyo nombre es un punto "
                "seguido de tu nombre de usuario (usa whoami).\n"
                "Búscalo en la carpeta 'archivo'. Los archivos ocultos solo se ven con ls -a."
            ),
            "documentos": {"notas.txt": "Pendientes: renovar el servidor, respaldar los logs."},
            "archivo": {
                "informe.txt": "Informe trimestral: sin novedades.",
                ".alumno": "PASSWORD: 0cult0_4lumn0",
                ".temporal": "(vacío)",
            },
        },
        "solucion": ["whoami", "cd archivo", "ls -a", "cat .alumno"],
    },
    # Subtema 2 · Creación y manipulación de archivos: mkdir, touch, cp, mv, rm
    "archivos": {
        "nivel": 2,
        "subtema": "Creación y manipulación de archivos",
        "titulo": "La bóveda",
        "instrucciones": "El guardia solo revela la contraseña cuando la bóveda está en orden.",
        "bitcoins": 75,
        "clave": "c0pi4_s3gur4",
        "usuario": "alumno",
        "comandos": ["help", "clear", "ls", "cd", "cat", "mkdir", "touch", "cp", "mv", "rm"],
        "sistema": {
            "readme.txt": (
                "Deja la bóveda en orden y el guardia te dará la contraseña:\n"
                "1. Crea la carpeta 'boveda'.\n"
                "2. Mueve 'llave.tmp' a 'boveda' con el nombre 'llave.txt'.\n"
                "3. Haz una copia de esa llave llamada 'respaldo.txt' dentro de 'boveda'.\n"
                "4. Crea el archivo vacío 'registro.txt' en 'boveda'.\n"
                "5. Borra 'basura.txt'.\n"
                "Después lee boveda/acceso.txt."
            ),
            "llave.tmp": "llave maestra",
            "basura.txt": "ruido sin importancia",
        },
        "disparadores": [{
            "requiere": ["boveda/llave.txt", "boveda/respaldo.txt", "boveda/registro.txt"],
            "ausentes": ["llave.tmp", "basura.txt"],
            "crea": {"boveda/acceso.txt": "PASSWORD: c0pi4_s3gur4"},
        }],
        "solucion": [
            "mkdir boveda", "mv llave.tmp boveda/llave.txt", "cp boveda/llave.txt boveda/respaldo.txt",
            "touch boveda/registro.txt", "rm basura.txt", "cat boveda/acceso.txt",
        ],
    },
    # Subtema 3 · Lectura y filtrado de información: cat, grep, head, tail, wc
    "filtrado": {
        "nivel": 3,
        "subtema": "Lectura y filtrado de información",
        "titulo": "El log interminable",
        "instrucciones": "La contraseña está enterrada en un registro enorme. No lo leas todo: fíltralo.",
        "bitcoins": 100,
        "clave": "gr3p_t4rg3t",
        "usuario": "alumno",
        "comandos": ["help", "clear", "ls", "cd", "cat", "grep", "head", "tail", "wc"],
        "sistema": {
            "readme.txt": (
                "El archivo logs/servidor.log tiene demasiadas líneas para leerlo completo.\n"
                "Cuenta sus líneas con wc -l, mira el inicio con head y el final con tail,\n"
                "y filtra con grep (también puedes encadenar comandos con |).\n"
                "La contraseña válida es la que lleva la etiqueta [ADMIN]."
            ),
            "logs": {"servidor.log": _LOG, "vacio.log": ""},
        },
        "solucion": ["cd logs", "wc -l servidor.log", "grep PASSWORD servidor.log", "cat servidor.log | grep ADMIN"],
    },
    # Subtema 4 · Búsqueda avanzada: find, locate, strings
    "busqueda": {
        "nivel": 4,
        "subtema": "Búsqueda avanzada",
        "titulo": "Aguja en el pajar",
        "instrucciones": "La contraseña está dentro de un programa perdido en el sistema.",
        "bitcoins": 125,
        "clave": "f1nd_str1ngs",
        "usuario": "alumno",
        "comandos": ["help", "clear", "ls", "cd", "cat", "find", "locate", "strings"],
        "sistema": {
            "readme.txt": (
                "Hay un programa llamado puerta.bin escondido en alguna carpeta.\n"
                "Encuéntralo con find o locate. Los programas no se leen con cat: "
                "strings extrae el texto legible."
            ),
            "sistema": {
                "opt": {
                    "herramientas": {
                        "puerta.bin": "\x7fELF\x02\x01\x00\x00\xff\xfe@@\x00PASSWORD: f1nd_str1ngs\x00\x00\xde\xad\xbe\xef",
                        "util.bin": "\x7fELF\x02\x01\x00\x00\xff\xfe\x00versi\xf3n 1.0\x00\x00",
                    },
                },
                "var": {"cache": {"datos.tmp": "sin datos"}},
            },
            "documentos": {"notas.txt": "Nada útil por aquí."},
        },
        "solucion": ["find . -name puerta.bin", "locate puerta.bin",
                     "strings sistema/opt/herramientas/puerta.bin"],
    },
    # Subtema 5 · Permisos y propiedad: chmod, su, chown
    "permisos": {
        "nivel": 5,
        "subtema": "Permisos y propiedad",
        "titulo": "Acceso denegado",
        "instrucciones": "El archivo con la contraseña existe, pero no te pertenece ni puedes leerlo.",
        "bitcoins": 150,
        "clave": "ch0wn_r00t",
        "usuario": "alumno",
        "comandos": ["help", "clear", "ls", "cd", "cat", "whoami", "chmod", "su", "chown"],
        "sistema": {
            "readme.txt": (
                "secreto.txt tiene la contraseña, pero cat te dirá 'Permiso denegado'.\n"
                "Mira sus permisos con ls -l. Solo la cuenta 'admin' puede cambiar dueño y "
                "permisos; su clave está en notas.txt."
            ),
            "notas.txt": "Cuenta admin -> clave: adm1n_2026",
            "secreto.txt": "PASSWORD: ch0wn_r00t",
        },
        "usuarios": {"alumno": None, "admin": "adm1n_2026"},
        "administradores": ["admin"],
        # modo en octal (dueño/grupo/otros). Se lee si el bit 4 aplica al que lo intenta
        # (dueño si es el mismo usuario; si no, "otros").
        "permisos": {"secreto.txt": {"dueno": "root", "modo": "000"}},
        # La contraseña de `su` se escribe en la línea siguiente.
        "solucion": ["su admin", "adm1n_2026", "chown admin secreto.txt",
                     "chmod 600 secreto.txt", "cat secreto.txt"],
    },
}

EJERCICIOS = NIVELES

LIMITE_COMANDO = 200  # caracteres; evita entradas absurdas
LIMITE_NODOS = 200    # archivos y carpetas que el alumno puede tener en total
LIMITE_NOMBRE = 40
LIMITE_TUBERIA = 3

DESCRIPCIONES = {
    "help": "help                  - Muestra esta ayuda",
    "clear": "clear                 - Limpia la pantalla",
    "pwd": "pwd                   - Muestra en qué carpeta estás",
    "whoami": "whoami                - Muestra tu nombre de usuario",
    "ls": "ls [-a] [-l] [dir]    - Lista archivos (-a ocultos, -l permisos y dueño)",
    "cd": "cd <dir>              - Cambia de carpeta ('cd ..' para regresar)",
    "cat": "cat <file>            - Muestra el contenido de un archivo",
    "mkdir": "mkdir <dir>           - Crea una carpeta",
    "touch": "touch <file>          - Crea un archivo vacío",
    "cp": "cp <origen> <destino> - Copia un archivo",
    "mv": "mv <origen> <destino> - Mueve o renombra",
    "rm": "rm <file>             - Borra un archivo",
    "grep": "grep [-i] [-n] [-c] <texto> [file] - Muestra las líneas que contienen el texto",
    "head": "head [-n N] [file]    - Primeras N líneas (10 por defecto)",
    "tail": "tail [-n N] [file]    - Últimas N líneas (10 por defecto)",
    "wc": "wc [-l] [-w] [-c] [file] - Cuenta líneas, palabras y bytes",
    "find": "find [dir] -name <patrón> [-type f|d] - Busca por nombre",
    "locate": "locate <texto>        - Busca en todo el sistema por la ruta",
    "strings": "strings <file>        - Extrae el texto legible de un archivo binario",
    "chmod": "chmod <modo> <file>   - Cambia permisos (ej. 644, u+r)",
    "su": "su <usuario>          - Cambia de usuario",
    "chown": "chown <usuario> <file> - Cambia el dueño de un archivo",
}


def ayuda(ejercicio):
    """Solo lista los comandos habilitados del nivel."""
    lineas = [DESCRIPCIONES[c] for c in ejercicio["comandos"] if c in DESCRIPCIONES]
    return "Comandos disponibles:\n" + "\n".join(f"  {l}" for l in lineas)


# --- Estado de la partida (vive en la sesión del alumno) ---------------------------

def estado_inicial(ejercicio):
    return {
        "ruta": [],                                        # carpeta actual, bajo ~
        "sistema": deepcopy(ejercicio["sistema"]),         # el alumno puede modificarlo
        "usuario": ejercicio["usuario"],
        "permisos": deepcopy(ejercicio.get("permisos", {})),
        "su": None,                                        # cuenta esperando su clave
        "hechos": [],                                      # disparadores ya cumplidos
    }


def _usuarios(ejercicio):
    return ejercicio.get("usuarios", {ejercicio["usuario"]: None})


def estado_valido(ejercicio, estado):
    """Comprueba lo que viene de la sesión antes de usarlo."""
    try:
        return (
            isinstance(estado["sistema"], dict)
            and estado["usuario"] in _usuarios(ejercicio)
            and isinstance(estado["permisos"], dict)
            and estado["su"] in (None, *_usuarios(ejercicio))
            and isinstance(estado["hechos"], list)
            and isinstance(estado["ruta"], list)
            and all(isinstance(p, str) for p in estado["ruta"])
            and isinstance(_nodo(estado["sistema"], estado["ruta"]), dict)
        )
    except (KeyError, TypeError):
        return False


# --- Lo que ve el navegador ---------------------------------------------------

def ruta_texto(ruta):
    """['documentos'] -> '~/documentos'; [] -> '~'."""
    return "~" + "".join(f"/{parte}" for parte in ruta)


def prompt(estado):
    return f"{estado['usuario']}@system:{ruta_texto(estado['ruta'])} $"


def datos_publicos(ejercicio):
    """Sin sistema de archivos ni contraseña."""
    return {"prompt": f"{ejercicio['usuario']}@system:~ $"}


# --- Sistema de archivos simulado ---------------------------------------------

def _nodo(sistema, ruta):
    """Nodo (str o dict) en `ruta` (lista de nombres bajo ~) o None."""
    nodo = sistema
    for parte in ruta:
        if not isinstance(nodo, dict) or parte not in nodo:
            return None
        nodo = nodo[parte]
    return nodo


def _home(ejercicio):
    return f"/home/{ejercicio['usuario']}"


def _resolver(ejercicio, actual, texto):
    """Combina la ruta actual con lo que escribió el alumno ('..', 'a/b', '~',
    o la ruta absoluta de su carpeta). Devuelve una lista, o None si la ruta
    queda fuera de ~ (el sistema simulado no tiene otra raíz)."""
    home = _home(ejercicio)
    if texto == home or texto.startswith(home + "/"):
        texto = "~" + texto[len(home):]
    if texto.startswith("~"):
        ruta, texto = [], texto[1:]
    elif texto.startswith("/"):
        return None
    else:
        ruta = list(actual)
    for parte in texto.split("/"):
        if parte in ("", "."):
            continue
        if parte == "..":
            if ruta:
                ruta.pop()
            continue
        ruta.append(parte)
    return ruta


def _recorrer(nodo, prefijo):
    """Todo lo que cuelga de `nodo`: (ruta_texto, nodo), en orden."""
    yield prefijo, nodo
    if isinstance(nodo, dict):
        for nombre in sorted(nodo):
            yield from _recorrer(nodo[nombre], f"{prefijo}/{nombre}")


def _contar(nodo):
    return 1 + (sum(_contar(h) for h in nodo.values()) if isinstance(nodo, dict) else 0)


# --- Permisos -----------------------------------------------------------------------

def _perm(ejercicio, estado, ruta, es_dir):
    p = estado["permisos"].get("/".join(ruta))
    if p:
        return p
    return {"dueno": ejercicio["usuario"], "modo": "755" if es_dir else "644"}


def _puede_leer(ejercicio, estado, ruta):
    p = _perm(ejercicio, estado, ruta, False)
    digito = p["modo"][0] if estado["usuario"] == p["dueno"] else p["modo"][2]
    return bool(int(digito) & 4)


def _modo_texto(modo, es_dir):
    return ("d" if es_dir else "-") + "".join(
        ("r" if int(d) & 4 else "-") + ("w" if int(d) & 2 else "-") + ("x" if int(d) & 1 else "-")
        for d in modo
    )


def _es_admin(ejercicio, estado):
    return estado["usuario"] in ejercicio.get("administradores", [])


def _nuevo_modo(actual, texto):
    """Aplica '644' o '+r', 'u-w', 'go=rx'... Devuelve el modo nuevo o None."""
    if re.fullmatch(r"[0-7]{3}", texto):
        return texto
    m = re.fullmatch(r"([ugoa]*)([+\-=])([rwx]+)", texto)
    if not m:
        return None
    quienes, op, permisos = m.groups()
    clases = "ugo" if quienes in ("", "a") or "a" in quienes else quienes
    bits = sum({"r": 4, "w": 2, "x": 1}[c] for c in set(permisos))
    digitos = []
    for i, c in enumerate("ugo"):
        d = int(actual[i])
        if c in clases:
            d = d | bits if op == "+" else d & (7 & ~bits) if op == "-" else bits
        digitos.append(str(d))
    return "".join(digitos)


# --- Utilidades de los comandos ---------------------------------------------------

def _resolver_nodo(ejercicio, estado, texto):
    ruta = _resolver(ejercicio, estado["ruta"], texto)
    nodo = _nodo(estado["sistema"], ruta) if ruta is not None else None
    return ruta, nodo


def _leer(ejercicio, estado, cmd, texto):
    """Contenido de un archivo o un mensaje de error: (contenido, error)."""
    ruta, nodo = _resolver_nodo(ejercicio, estado, texto)
    if nodo is None:
        return None, f"{cmd}: {texto}: No existe el archivo o directorio"
    if isinstance(nodo, dict):
        return None, f"{cmd}: {texto}: Es un directorio"
    if not _puede_leer(ejercicio, estado, ruta):
        return None, f"{cmd}: {texto}: Permiso denegado"
    return nodo, None


def _es_binario(texto):
    return "\x00" in texto


def _texto_de(ejercicio, estado, cmd, archivos, entrada, uso):
    """Entrada de los filtros: el archivo dado o lo que viene por tubería."""
    if len(archivos) > 1:
        return None, uso
    if archivos:
        return _leer(ejercicio, estado, cmd, archivos[0])
    if entrada is not None:
        return entrada, None
    return None, uso


def _crear(ejercicio, estado, cmd, texto, valor, que):
    """Crea un archivo o carpeta vacío. Devuelve un mensaje de error o None."""
    ruta = _resolver(ejercicio, estado["ruta"], texto)
    if not ruta:
        return f"{cmd}: no se puede crear {que} '{texto}': ruta inválida"
    if _nodo(estado["sistema"], ruta) is not None:
        return f"{cmd}: no se puede crear {que} '{texto}': El archivo ya existe"
    padre = _nodo(estado["sistema"], ruta[:-1])
    if not isinstance(padre, dict):
        return f"{cmd}: no se puede crear {que} '{texto}': No existe el archivo o directorio"
    return _poner(estado, padre, ruta[-1], valor, cmd, texto)


def _poner(estado, padre, nombre, valor, cmd, texto):
    if len(nombre) > LIMITE_NOMBRE:
        return f"{cmd}: '{texto}': Nombre demasiado largo"
    if nombre not in padre and _contar(estado["sistema"]) >= LIMITE_NODOS:
        return f"{cmd}: '{texto}': No hay espacio en el sistema"
    padre[nombre] = valor
    return None


def _sin_opciones(cmd, args):
    for a in args:
        if a.startswith("-") and len(a) > 1:
            return f"{cmd}: opción no soportada: {a}"
    return None


# --- Comandos: cada uno devuelve (salida, es_error) --------------------------------

def _help(ej, est, args, entrada):
    return ayuda(ej), False


def _pwd(ej, est, args, entrada):
    return _home(ej) + "".join(f"/{p}" for p in est["ruta"]), False


def _whoami(ej, est, args, entrada):
    return est["usuario"], False


def _ls(ej, est, args, entrada):
    banderas = {c for a in args if a.startswith("-") for c in a[1:]}
    rutas = [a for a in args if not a.startswith("-")]
    if not banderas <= {"a", "l"} or len(rutas) > 1:
        return "Uso: ls [-a] [-l] [directorio]", True
    texto = rutas[0] if rutas else "."
    ruta, nodo = _resolver_nodo(ej, est, texto)
    if nodo is None:
        return f"ls: no existe el archivo o directorio: {texto}", True
    if isinstance(nodo, str):
        entradas = [(texto, nodo, ruta)]
    else:
        nombres = sorted(n for n in nodo if "a" in banderas or not n.startswith("."))
        entradas = [(n, nodo[n], ruta + [n]) for n in nombres]
    if not entradas:
        return "(directorio vacío)", False
    if "l" in banderas:
        filas = []
        for nombre, hijo, r in entradas:
            es_dir = isinstance(hijo, dict)
            p = _perm(ej, est, r, es_dir)
            filas.append(f"{_modo_texto(p['modo'], es_dir)} {p['dueno']} {nombre}{'/' if es_dir else ''}")
        return "\n".join(filas), False
    return "  ".join(f"{n}/" if isinstance(h, dict) else n for n, h, _ in entradas), False


def _cd(ej, est, args, entrada):
    if len(args) > 1:
        return "cd: demasiados argumentos", True
    ruta, nodo = _resolver_nodo(ej, est, args[0]) if args else ([], est["sistema"])
    if nodo is None:
        return f"cd: no existe el archivo o directorio: {args[0]}", True
    if isinstance(nodo, str):
        return f"cd: {args[0]}: No es un directorio", True
    est["ruta"] = ruta
    return "", False


def _cat(ej, est, args, entrada):
    if len(args) != 1:
        return "Uso: cat <archivo>", True
    texto, error = _leer(ej, est, "cat", args[0])
    if error:
        return error, True
    if _es_binario(texto):
        return f"cat: {args[0]}: es un archivo binario (prueba con strings)", True
    return texto, False


def _mkdir(ej, est, args, entrada):
    error = _sin_opciones("mkdir", args) or (None if args else "Uso: mkdir <carpeta>")
    for texto in ([] if error else args):
        error = _crear(ej, est, "mkdir", texto, {}, "el directorio")
        if error:
            break
    return (error, True) if error else ("", False)


def _touch(ej, est, args, entrada):
    error = _sin_opciones("touch", args) or (None if args else "Uso: touch <archivo>")
    for texto in ([] if error else args):
        ruta, nodo = _resolver_nodo(ej, est, texto)
        if nodo is not None:
            continue  # ya existe: no pasa nada
        error = _crear(ej, est, "touch", texto, "", "el archivo")
        if error:
            break
    return (error, True) if error else ("", False)


def _destino(ej, est, cmd, origen_ruta, origen_nodo, texto):
    """Ruta final de cp/mv: dentro de la carpeta si el destino es una; si no, el nombre dado."""
    ruta, nodo = _resolver_nodo(ej, est, texto)
    if ruta is None or not ruta and nodo is None:
        return None, f"{cmd}: '{texto}': ruta inválida"
    if isinstance(nodo, dict):
        ruta = ruta + [origen_ruta[-1]]
        nodo = _nodo(est["sistema"], ruta)
    if isinstance(nodo, dict):
        return None, f"{cmd}: no se puede sobrescribir el directorio '{texto}'"
    padre = _nodo(est["sistema"], ruta[:-1])
    if not isinstance(padre, dict):
        return None, f"{cmd}: no se puede crear '{texto}': No existe el archivo o directorio"
    if ruta == origen_ruta:
        return None, f"{cmd}: '{texto}' y el origen son el mismo archivo"
    return ruta, None


def _cp(ej, est, args, entrada):
    error = _sin_opciones("cp", args)
    if error:
        return error, True
    if len(args) != 2:
        return "Uso: cp <origen> <destino>", True
    contenido, error = _leer(ej, est, "cp", args[0])
    if error:
        return error, True
    origen = _resolver(ej, est["ruta"], args[0])
    destino, error = _destino(ej, est, "cp", origen, contenido, args[1])
    if error:
        return error, True
    error = _poner(est, _nodo(est["sistema"], destino[:-1]), destino[-1], contenido, "cp", args[1])
    return (error, True) if error else ("", False)


def _mv(ej, est, args, entrada):
    error = _sin_opciones("mv", args)
    if error:
        return error, True
    if len(args) != 2:
        return "Uso: mv <origen> <destino>", True
    origen, nodo = _resolver_nodo(ej, est, args[0])
    if nodo is None:
        return f"mv: no se puede mover '{args[0]}': No existe el archivo o directorio", True
    if not origen:
        return "mv: no se puede mover tu carpeta personal", True
    destino, error = _destino(ej, est, "mv", origen, nodo, args[1])
    if error:
        return error, True
    if isinstance(nodo, dict) and destino[:len(origen)] == origen:
        return f"mv: no se puede mover '{args[0]}' a un subdirectorio de sí mismo", True
    padre_destino = _nodo(est["sistema"], destino[:-1])
    error = _poner(est, padre_destino, destino[-1], nodo, "mv", args[1])
    if error:
        return error, True
    del _nodo(est["sistema"], origen[:-1])[origen[-1]]
    return "", False


def _rm(ej, est, args, entrada):
    error = _sin_opciones("rm", args) or (None if args else "Uso: rm <archivo>")
    if error:
        return error, True
    for texto in args:
        ruta, nodo = _resolver_nodo(ej, est, texto)
        if nodo is None:
            return f"rm: no se puede borrar '{texto}': No existe el archivo o directorio", True
        if isinstance(nodo, dict):
            return f"rm: no se puede borrar '{texto}': Es un directorio", True
        del _nodo(est["sistema"], ruta[:-1])[ruta[-1]]
    return "", False


def _grep(ej, est, args, entrada):
    uso = "Uso: grep [-i] [-n] [-c] <texto> [archivo]"
    banderas, resto = set(), list(args)
    while resto and resto[0].startswith("-") and len(resto[0]) > 1:
        banderas |= set(resto.pop(0)[1:])
    if not banderas <= {"i", "n", "c"} or not resto:
        return uso, True
    patron, archivos = resto[0], resto[1:]
    texto, error = _texto_de(ej, est, "grep", archivos, entrada, uso)
    if error:
        return error, True
    if _es_binario(texto):
        return f"grep: {archivos[0]}: el archivo es binario", True
    buscado = patron.lower() if "i" in banderas else patron
    hallazgos = [
        (n, linea) for n, linea in enumerate(texto.splitlines(), 1)
        if buscado in (linea.lower() if "i" in banderas else linea)
    ]
    if "c" in banderas:
        return str(len(hallazgos)), False
    return "\n".join(f"{n}:{l}" if "n" in banderas else l for n, l in hallazgos), False


def _cabeza_cola(nombre):
    def comando(ej, est, args, entrada):
        uso = f"Uso: {nombre} [-n N] [archivo]"
        n, resto = 10, list(args)
        if resto and resto[0] == "-n":
            if len(resto) < 2 or not resto[1].isdigit():
                return f"{nombre}: número de líneas inválido", True
            n, resto = int(resto[1]), resto[2:]
        elif resto and re.fullmatch(r"-\d+", resto[0]):
            n, resto = int(resto[0][1:]), resto[1:]
        if resto and resto[0].startswith("-") and len(resto[0]) > 1:
            return uso, True
        texto, error = _texto_de(ej, est, nombre, resto, entrada, uso)
        if error:
            return error, True
        lineas = texto.splitlines()
        elegidas = (lineas[:n] if nombre == "head" else lineas[len(lineas) - n:] if n else [])
        return "\n".join(elegidas), False
    return comando


def _wc(ej, est, args, entrada):
    uso = "Uso: wc [-l] [-w] [-c] [archivo]"
    banderas = {c for a in args if a.startswith("-") for c in a[1:]}
    archivos = [a for a in args if not a.startswith("-")]
    if not banderas <= {"l", "w", "c"}:
        return uso, True
    texto, error = _texto_de(ej, est, "wc", archivos, entrada, uso)
    if error:
        return error, True
    cuentas = {"l": len(texto.splitlines()), "w": len(texto.split()), "c": len(texto.encode())}
    quedan = [c for c in "lwc" if c in banderas] or list("lwc")
    partes = [str(cuentas[c]) for c in quedan] + (archivos[:1])
    return " ".join(partes), False


def _strings(ej, est, args, entrada):
    uso = "Uso: strings <archivo>"
    texto, error = _texto_de(ej, est, "strings", args, entrada, uso)
    if error:
        return error, True
    return "\n".join(re.findall(r"[ -~]{4,}", texto)), False


def _find(ej, est, args, entrada):
    uso = "Uso: find [directorio] -name <patrón> [-type f|d]"
    base = patron = tipo = None
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("-name", "-type"):
            if i + 1 >= len(args):
                return uso, True
            if a == "-name":
                patron = args[i + 1]
            else:
                tipo = args[i + 1]
                if tipo not in ("f", "d"):
                    return uso, True
            i += 2
        elif a.startswith("-") or base is not None:
            return uso, True
        else:
            base, i = a, i + 1
    base = base or "."
    ruta, nodo = _resolver_nodo(ej, est, base)
    if nodo is None:
        return f"find: '{base}': No existe el archivo o directorio", True
    prefijo = base.rstrip("/") or base
    salida = []
    for texto, hijo in _recorrer(nodo, prefijo):
        if patron and not fnmatch.fnmatchcase(texto.rsplit("/", 1)[-1], patron):
            continue
        if tipo and (tipo == "d") != isinstance(hijo, dict):
            continue
        salida.append(texto)
    return "\n".join(salida), False


def _locate(ej, est, args, entrada):
    if len(args) != 1 or args[0].startswith("-"):
        return "Uso: locate <texto>", True
    patron = args[0]
    salida = []
    for texto, _ in _recorrer(est["sistema"], _home(ej)):
        if texto == _home(ej):
            continue
        coincide = (fnmatch.fnmatchcase(texto, f"*{patron}*") if re.search(r"[*?\[]", patron)
                    else patron in texto)
        if coincide:
            salida.append(texto)
    return "\n".join(salida), False


def _chmod(ej, est, args, entrada):
    if len(args) != 2:
        return "Uso: chmod <modo> <archivo>", True
    modo_txt, texto = args
    ruta, nodo = _resolver_nodo(ej, est, texto)
    if nodo is None or not ruta:
        return f"chmod: no se puede acceder a '{texto}': No existe el archivo o directorio", True
    p = _perm(ej, est, ruta, isinstance(nodo, dict))
    nuevo = _nuevo_modo(p["modo"], modo_txt)
    if nuevo is None:
        return f"chmod: modo inválido: '{modo_txt}'", True
    if not (_es_admin(ej, est) or est["usuario"] == p["dueno"]):
        return f"chmod: cambiando permisos de '{texto}': Operación no permitida", True
    est["permisos"]["/".join(ruta)] = {"dueno": p["dueno"], "modo": nuevo}
    return "", False


def _chown(ej, est, args, entrada):
    if len(args) != 2:
        return "Uso: chown <usuario> <archivo>", True
    dueno, texto = args
    ruta, nodo = _resolver_nodo(ej, est, texto)
    if nodo is None or not ruta:
        return f"chown: no se puede acceder a '{texto}': No existe el archivo o directorio", True
    if not _es_admin(ej, est):
        return f"chown: cambiando propietario de '{texto}': Operación no permitida", True
    if dueno not in _usuarios(ej):
        return f"chown: usuario inválido: '{dueno}'", True
    p = _perm(ej, est, ruta, isinstance(nodo, dict))
    est["permisos"]["/".join(ruta)] = {"dueno": dueno, "modo": p["modo"]}
    return "", False


def _su(ej, est, args, entrada):
    if len(args) != 1:
        return "Uso: su <usuario>", True
    objetivo, usuarios = args[0], _usuarios(ej)
    if objetivo not in usuarios:
        return f"su: el usuario {objetivo} no existe", True
    if objetivo == est["usuario"]:
        return "", False
    if usuarios[objetivo] is None:
        est["usuario"] = objetivo  # esa cuenta no pide clave
    else:
        est["su"] = objetivo       # la clave llega en la siguiente línea
    return "", False


COMANDOS = {
    "help": _help, "pwd": _pwd, "whoami": _whoami, "ls": _ls, "cd": _cd, "cat": _cat,
    "mkdir": _mkdir, "touch": _touch, "cp": _cp, "mv": _mv, "rm": _rm,
    "grep": _grep, "head": _cabeza_cola("head"), "tail": _cabeza_cola("tail"), "wc": _wc,
    "find": _find, "locate": _locate, "strings": _strings,
    "chmod": _chmod, "su": _su, "chown": _chown,
}  # clear lo resuelve ejecutar()


# --- Intérprete -----------------------------------------------------------------

def _disparar(ejercicio, estado):
    """Revisa los disparadores del nivel y devuelve los avisos de lo que apareció."""
    avisos = []
    for i, d in enumerate(ejercicio.get("disparadores", [])):
        if i in estado["hechos"]:
            continue
        if not all(isinstance(_nodo(estado["sistema"], r.split("/")), str) for r in d["requiere"]):
            continue
        if any(_nodo(estado["sistema"], r.split("/")) is not None for r in d["ausentes"]):
            continue
        for ruta, contenido in d["crea"].items():
            partes = ruta.split("/")
            padre = _nodo(estado["sistema"], partes[:-1])
            if isinstance(padre, dict):
                padre[partes[-1]] = contenido
                avisos.append(f"[sistema] Apareció un archivo nuevo: {ruta}")
        estado["hechos"].append(i)
    return avisos


def ejecutar(ejercicio, estado, linea):
    """Interpreta una línea (con tuberías '|') y modifica `estado`.

    Devuelve un dict:
      salida  - texto a mostrar ("" si no hay)
      error   - True si la salida es un mensaje de error (FA-1 / FA-2)
      limpiar - True si hay que vaciar la pantalla (clear)
      oculto  - True si la siguiente línea es una contraseña (su): no debe mostrarse
    """
    resp = {"salida": "", "error": False, "limpiar": False, "oculto": False}

    def listo():
        resp["oculto"] = estado["su"] is not None
        return resp

    def falla(texto):
        resp["salida"], resp["error"] = texto, True
        return listo()

    # La línea siguiente a `su <usuario>` es la contraseña de esa cuenta.
    if estado["su"]:
        objetivo, estado["su"] = estado["su"], None
        clave = _usuarios(ejercicio)[objetivo]
        if hmac.compare_digest(linea.strip().encode(), clave.encode()):
            estado["usuario"] = objetivo
            return listo()
        return falla("su: Falló la autenticación")

    if not linea.strip():
        return listo()  # solo Enter: nuevo prompt (FA-1)
    try:
        segmentos = [shlex.split(s) for s in linea.split("|")]
    except ValueError:
        return falla("Comando mal formado: revisa las comillas.")
    if any(not s for s in segmentos):
        return falla("Comando mal formado: falta un comando junto a |.")
    if len(segmentos) > LIMITE_TUBERIA:
        return falla("Demasiados comandos encadenados.")

    entrada = None
    for partes in segmentos:
        comando, args = partes[0], partes[1:]
        if comando not in ejercicio["comandos"] or (comando not in COMANDOS and comando != "clear"):
            return falla(f"Comando no encontrado: {comando}. Escribe 'help' para ver los comandos.")
        if comando == "clear":
            resp["limpiar"] = True
            entrada = ""
            continue
        salida, error = COMANDOS[comando](ejercicio, estado, args, entrada)
        if error:
            return falla(salida)
        entrada = salida

    avisos = _disparar(ejercicio, estado)
    resp["salida"] = "\n".join(([entrada] if entrada else []) + avisos)
    return listo()


# --- La puerta --------------------------------------------------------------------

def revisar_clave(ejercicio, texto):
    """Compara lo que escribió el alumno con la contraseña (distingue
    mayúsculas). Acepta también la línea completa copiada: 'PASSWORD: ...'."""
    texto = texto.strip()
    if texto.upper().startswith("PASSWORD:"):
        texto = texto[len("PASSWORD:"):].strip()
    return hmac.compare_digest(texto.encode(), ejercicio["clave"].encode())