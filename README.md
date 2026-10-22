# Re:Code — Tetra.R

Novela visual educativa de terror psicológico. Django (MTV) + SQLite + Monogatari, en Docker.

Este README es la guía de operación: cómo levantar el proyecto, configurarlo, desplegarlo y darle mantenimiento. Lo que el sistema debe hacer está en el SRS y cómo está hecho por dentro, en el SCS.

## Estado del sprint 2

Están implementados los seis retos (CU05 a CU10), el mapa, la novela, Mi Perfil, el registro y el inicio de sesión. Quedan pendientes para el siguiente sprint la red corrupta (CU03, con su bloqueo de 3 minutos), la notificación de materia completada (R9), el jumpscare del examen (R41) y el mensaje de error de R53.

## Requisitos

- Docker Desktop abierto (opción recomendada), o bien Python 3.12.
- Dependencias (`requirements.txt`): Django 5.0, gunicorn y whitenoise.
- Un navegador actual y una conexión a internet estable.

## Levantarlo en tu compu

Con Docker Desktop abierto:

```bash
docker compose up --build
```

Entra a http://localhost:8000. Al arrancar se aplican las migraciones y se crea el alumno de prueba (usuario `prueba`, contraseña `test1234`). También puedes registrarte con tu propio usuario.

Para detenerlo, `Ctrl + C`; para apagar y quitar el contenedor, `docker compose down`.

### Sin Docker (opcional)

```bash
python -m venv .venv
source .venv/bin/activate        # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py crear_alumno_prueba
python manage.py runserver
```

## Configuración

Se hace con variables de entorno. Todas tienen valor por defecto para desarrollo.

| Variable | Para qué sirve | Por defecto |
|---|---|---|
| `SECRET_KEY` | Llave secreta de Django. En producción **debe** ser propia | una llave de desarrollo |
| `DEBUG` | `True` o `False`. En producción, `False` | `True` |
| `DOMINIO` | Dominio propio, si lo hay. Se agrega a los hosts permitidos y a los orígenes de confianza para CSRF | (vacío) |
| `SQLITE_PATH` | Ruta del archivo de la base de datos | `data/db.sqlite3` |
| `PORT` | Puerto en el que escucha gunicorn en producción | `8000` |

Los hosts `localhost`, `127.0.0.1` y `*.up.railway.app` ya vienen permitidos.

## Base de datos

- Es SQLite. El archivo está en `data/db.sqlite3` y no se sube al repositorio: cada quien tiene la suya.
- Para empezar de cero, apaga el contenedor y borra la carpeta `data/`.
- Solo `progreso` tiene modelos: `Progreso` (bitcoins), `RetoResuelto`, `IntentoExamen` y `NovelaVista`. El alumno es el `User` de Django.
- Las migraciones se generan a mano y se suben al repo. Si cambias `progreso/models.py`:

```bash
docker compose run --rm web python manage.py makemigrations
```

  Sube la migración junto con tu cambio.

## Operación del día a día

| Tarea | Comando |
|---|---|
| Ver los registros del servidor | `docker compose logs -f web` |
| Aplicar migraciones | `docker compose run --rm web python manage.py migrate` |
| Crear el alumno de prueba (si no existe) | `docker compose run --rm web python manage.py crear_alumno_prueba` |
| Crear un administrador | `docker compose run --rm web python manage.py createsuperuser` |
| Entrar al panel de administración | http://localhost:8000/admin/ |
| Reconstruir tras cambiar dependencias | `docker compose up --build` |

## Componentes

| App | Capa | Qué hace |
|---|---|---|
| `comun` | T | Plantilla base, plantilla de retos, JS que envía las respuestas y estilos |
| `progreso` | M V | **Único con modelos.** Guarda el avance (bitcoins, retos resueltos, exámenes, novelas vistas). Registro, Mi Perfil y API JSON |
| `mapa` | V T | Mapa de materias y pantalla de cada materia. Las materias y subtemas están en `mapa/temas.py` |
| `novela` | V T | Página de la novela con Monogatari |
| `batalla` | V T | Examen de cada materia y batalla final. Preguntas en `batalla/preguntas.py` |
| `reto_algebra_booleana` | V T | CU05: circuitos |
| `reto_comandos_linux` | V T | CU06: terminal Linux |
| `reto_ecuaciones` | V T | CU07: ecuaciones lineales (matriz) |
| `reto_clasificar` | V T | CU08: clasificar elementos por categorías |
| `reto_obtener_termino` | V T | CU09: término oculto |
| `reto_sopa_letras` | V T | CU10: sopa de letras |

Pendiente: `red_corrupta` (CU03). Aún no existe como app.

El alumno es el `User` que ya trae Django (tabla `auth_user`), así que no hay app de usuarios. El inicio y cierre de sesión usan las vistas de Django (`config/urls.py`) y el registro está en `progreso`, porque al crear la cuenta también se crea su progreso. Las demás apps no guardan nada directamente: llaman a las funciones de `progreso/servicios.py`.

## Rutas principales

| Ruta | Qué es |
|---|---|
| `/` | Mapa de materias |
| `/materia/{slug}/` | Selección de retos de una materia |
| `/entrar/` y `/salir/` | Inicio y cierre de sesión |
| `/retos/algebra-booleana/{ejercicio}/` | CU05 |
| `/retos/comandos-linux/{ejercicio}/` | CU06 |
| `/retos/ecuaciones/{ejercicio}/` | CU07 |
| `/retos/clasificar/{ejercicio}/` | CU08 |
| `/retos/obtener-termino/{ejercicio}/` | CU09 |
| `/retos/sopa-letras/{ejercicio}/` | CU10 |

Cada reto también expone sus peticiones POST (`revisar/`, `comando/`, `puerta/`, `reiniciar/`, `clasificar/`, `completar/`); están listadas en la sección 3.3 del SCS.

## Cómo está hecho un reto

Todas las apps de reto tienen la misma forma:

```
reto_xxx/
├── ejercicios.py      ← contenido y respuestas (solo en el servidor)
├── views.py           ← jugar (muestra la pantalla) y revisar (califica)
├── urls.py
├── templates/reto_xxx/reto.html   ← extiende comun/reto_base.html
└── static/reto_xxx/juego.js       ← la mecánica en el navegador
```

1. `ejercicios.py` define `EJERCICIOS` (título, bitcoins y pasos), `datos_publicos()` (lo que sí ve el navegador, **sin respuestas**) y `revisar_respuesta()` (la calificación).
2. `juego.js` dibuja el reto y, por cada respuesta del alumno, la envía al servidor.
3. La vista califica en el servidor y le pasa el resultado a `progreso`, que lleva la cuenta de pasos. Cuando están todos, registra el reto y da los bitcoins (solo la primera vez).

El reto de clasificar usa `clasificar()` y `completar()` en lugar de `revisar()`; la terminal Linux usa `comando()` y `puerta()`; el término oculto agrega `reiniciar()`.

### Agregar un ejercicio

Agrégalo en el `ejercicios.py` de su reto y apúntalo en el subtema que le toca en `mapa/temas.py`, como `("nombre_de_la_app", "id_del_ejercicio")`.

## Novela visual

Cada materia abre con su novela la primera vez. La historia de cada una va en `novela/static/novela/historias/<slug>.js` (por ejemplo `logica.js`). Si una materia no tiene la suya, se usa `generica.js`. Al final de cada historia va `terminarNovela()`, que avisa a `progreso` por JSON y regresa a la materia.

## Exámenes y batalla final

Hay un examen por materia, en `batalla/preguntas.py` (la llave es el slug de la materia), y uno `"final"`. Se califican en el servidor. La batalla final se abre cuando el alumno aprobó el examen de **todas** las materias, así que hasta que cada materia tenga su examen, la final no aparece.

## Despliegue (Railway)

El `Dockerfile` ejecuta `collectstatic` al construir y, al arrancar, aplica las migraciones y levanta gunicorn.

1. Conecta el repositorio al servicio web de Railway.
2. Define `SECRET_KEY` (propia) y `DEBUG=False`; si hay dominio propio, `DOMINIO`.
3. Agrega un **volumen montado en `/app/data`** al servicio web. Sin él, la base de datos se borra en cada despliegue.
4. Despliega. El sitio responde en el dominio `*.up.railway.app` que asigna Railway.

Para respaldar la base de datos, copia `data/db.sqlite3` del volumen.

## Flujo de trabajo en el equipo

- La rama `construction` es la integrada; el trabajo nuevo se hace en una rama propia y se une a `construction`.
- No subas `data/`, `staticfiles/` ni archivos `.sqlite3` (ya están en `.gitignore`).
- Si tocas modelos, sube también la migración.

## Problemas frecuentes

| Síntoma | Qué hacer |
|---|---|
| El puerto 8000 ya está ocupado | Cierra lo que lo use o cambia el puerto en `docker-compose.yml` (por ejemplo `"8001:8000"`) |
| Error de migraciones tras cambiar de rama | Borra `data/` y vuelve a levantar para empezar de cero |
| No puedo iniciar sesión | Usa `prueba` / `test1234`; si borraste `data/`, vuelve a levantar para que se cree de nuevo |
| El progreso desapareció en Railway | Falta el volumen en `/app/data` |
| Error CSRF en producción | Revisa que `DOMINIO` coincida con el dominio con el que entras |

## Despliegue temporal: PythonAnywhere

El 22/10/2026 Railway pausó los despliegues en toda su plataforma por una falla de un proveedor externo. Mientras se restablece, la app corre en PythonAnywhere (plan gratuito) desde la rama `construction`, sin cambios en el código. PythonAnywhere no usa Docker: las variables `SECRET_KEY`, `DEBUG=False` y `DOMINIO` se definen en su archivo WSGI, y la base SQLite queda en `data/db.sqlite3`.

Para actualizarla después de subir cambios (consola Bash de PythonAnywhere):

    cd ~/TSP_Tetra.R_Repositorio_A26 && source ~/venv/bin/activate
    git pull && python manage.py migrate && python manage.py collectstatic --noinput

Luego, en la pestaña Web, botón **Reload**.

Al volver a Railway, si se quieren conservar los alumnos registrados, descargar `data/db.sqlite3` desde la pestaña *Files* y subirlo al volumen montado en `/app/data`.