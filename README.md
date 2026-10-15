# Re:Code — Tetra.R

Novela visual educativa de terror psicológico. Django (MTV) + SQLite + Monogatari, en Docker.

## Levantarlo en tu compu

Con Docker Desktop abierto:

```bash
docker compose up --build
```

Entra a http://localhost:8000. Al arrancar se aplican las migraciones y se crea el alumno de prueba (usuario `prueba`, contraseña `test1234`). También puedes registrarte con tu propio usuario.

La base de datos es `data/db.sqlite3` y no se sube al repo: cada quien tiene la suya. Para empezar de cero, borra la carpeta `data/`.

Si cambias `progreso/models.py`, genera la migración y súbela junto con tu cambio:

```bash
docker compose run --rm web python manage.py makemigrations
```

## Componentes (igual que el diagrama)

| App | Capa | Qué hace |
|---|---|---|
| `comun` | T | Plantilla base, plantilla de retos, JS que envía las respuestas y estilos |
| `progreso` | M V | **Único con modelos.** Guarda el avance (bitcoins, retos resueltos, exámenes, novelas vistas). Registro, Mi Perfil y API JSON |
| `mapa` | V T | Mapa de materias y pantalla de cada materia. Las materias y subtemas están en `mapa/temas.py` |
| `novela` | V T | Página de la novela con Monogatari |
| `batalla` | V T | Examen de cada materia y batalla final. Preguntas en `batalla/preguntas.py` |
| `reto_algebra_booleana` | V T | CU-05 |
| `reto_comandos_linux` | V T | CU-06 |
| `reto_ecuaciones` | V T | CU-07 |
| `reto_desigualdades` | V T | CU-08 |
| `reto_obtener_termino` | V T | CU-09 |
| `reto_conceptos` | V T | CU-10 (sopa de letras) |

El alumno es el `User` que ya trae Django (tabla `auth_user`), así que no hay app de usuarios. El inicio y cierre de sesión usan las vistas de Django (`config/urls.py`) y el registro está en `progreso`, porque al crear la cuenta también se crea su progreso.

Las demás apps no guardan nada directamente: llaman a las funciones de `progreso/servicios.py`.

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
2. `juego.js` dibuja el reto y, por cada respuesta del alumno, llama a `ReCode.enviarRespuesta(paso, respuesta)`.
3. `views.revisar` califica en el servidor y le pasa el resultado a `progreso`, que lleva la cuenta de pasos. Cuando están todos, registra el reto y da los bitcoins (solo la primera vez).

Para agregar otro ejercicio a un reto, agrégalo en su `ejercicios.py` y apúntalo en el subtema que va en `mapa/temas.py`.

## Novela visual

Cada materia abre con su novela la primera vez. La historia de cada una va en `novela/static/novela/historias/<slug>.js` (por ejemplo `logica.js`). Si una materia no tiene la suya, se usa `generica.js`. Al final de cada historia va `terminarNovela()`, que avisa a `progreso` por JSON y regresa a la materia. Las imágenes y sonidos irían en `novela/static/novela/assets/`.

## Exámenes y batalla final

Uno por materia, en `batalla/preguntas.py` (la llave es el slug de la materia) y uno `"final"`. Se califican en el servidor. La batalla final se abre cuando el alumno aprobó el examen de **todas** las materias, así que hasta que cada materia tenga su examen, la final no aparece.

## Railway

El `Dockerfile` aplica las migraciones y arranca con gunicorn. Usa las variables `SECRET_KEY`, `DEBUG=False` y, si tienen dominio propio, `DOMINIO`. Para que la base de datos no se borre en cada despliegue hay que **agregar un volumen montado en `/app/data`** al servicio web. El servicio de MySQL ya no se usa.
