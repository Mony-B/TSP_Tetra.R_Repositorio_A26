from django.core.management.base import BaseCommand
from recode.models import Ruta, Subtema, RetoCF, RetoCifrado, RetoDD, RetoDecision, Alumno, ProgresoAlumno


class Command(BaseCommand):
    help = "Crea los datos de prueba de Lógica y Algoritmos + un alumno de prueba"

    def handle(self, *args, **options):
        ruta, _ = Ruta.objects.get_or_create(
            nombre_ruta="Lógica y Algoritmos", slug="logica"
        )
        Ruta.objects.get_or_create(nombre_ruta="Introducción a la Programación", slug="introprog")
        Ruta.objects.get_or_create(nombre_ruta="Linux", slug="linux")
        Ruta.objects.get_or_create(nombre_ruta="Cálculo", slug="calculo")
        Ruta.objects.get_or_create(nombre_ruta="Álgebra", slug="algebra")

        s1, _ = Subtema.objects.get_or_create(nombre_subtema="Algoritmos", ruta=ruta, orden=1)
        s2, _ = Subtema.objects.get_or_create(nombre_subtema="Lógica proposicional", ruta=ruta, orden=2)
        s3, _ = Subtema.objects.get_or_create(nombre_subtema="Conjuntos y Leyes de Morgan", ruta=ruta, orden=3)

        if not s1.retos.exists():
            RetoCF.objects.create(
                subtema=s1, orden=1, recompensa_exp=30,
                estructura_frase={"texto": "1) Abrir la tabla de planchar, 2) ___, 3) Colocar la camisa sobre la tabla",
                                   "blanks": ["Rellenar la plancha de agua y encenderla"]},
                pista="Antes de planchar necesitas preparar la plancha misma.",
                retro_incorrecta="Recuerda: antes de planchar, hay que llenar de agua y encender la plancha.",
                retro_correcta="¡Correcto! Ese es el paso de preparación.",
            )
            RetoCF.objects.create(
                subtema=s1, orden=2, recompensa_exp=50,
                estructura_frase={"texto": "1) Encender el ordenador, 2) ___, 3) Encender la impresora, 4) ___, 5) Seleccionar Imprimir",
                                   "blanks": ["Asegurarnos de que la impresora tiene papel y cartuchos de tinta",
                                              "Abrir el documento que queremos imprimir"]},
                pista="Piensa en qué revisarías físicamente en la impresora, y qué archivo necesitas tener abierto.",
                retro_incorrecta="Antes de imprimir hay que revisar que la impresora tenga insumos, y abrir el documento deseado.",
                retro_correcta="¡Bien! Preparación + selección del archivo.",
            )
            RetoCF.objects.create(
                subtema=s1, orden=3, recompensa_exp=70,
                estructura_frase={"texto": "Las tres partes de un algoritmo son: ___ (lo que recibe), ___ (los pasos) y ___ (el resultado)",
                                   "blanks": ["Input", "Proceso", "Output"]},
                pista="Son las 3 fases por las que pasa la información: lo que entra, lo que se hace, lo que sale.",
                retro_incorrecta="Las tres partes son: Input, Proceso y Output (en ese orden).",
                retro_correcta="¡Exacto! Input → Proceso → Output.",
            )

        if not s2.retos.exists():
            RetoCifrado.objects.create(
                subtema=s2, orden=1, recompensa_exp=30,
                acertijo_logico={"mensaje_cifrado": "p=1, q=0. Calcula p ∧ q", "respuesta": "0"},
                pista="La conjunción (∧) solo es verdadera (1) cuando AMBOS valores son 1.",
                retro_incorrecta="p∧q es verdadero solo si p=1 Y q=1. Aquí q=0, así que el resultado es 0.",
                retro_correcta="¡Correcto! Con q=0, la conjunción da 0 sin importar p.",
            )
            RetoCifrado.objects.create(
                subtema=s2, orden=2, recompensa_exp=50,
                acertijo_logico={"mensaje_cifrado": "p=0, q=1. Calcula ¬p ∨ q", "respuesta": "1"},
                pista="Primero niega p, luego aplica disyunción (∨): basta con que UNO de los dos sea 1.",
                retro_incorrecta="¬p invierte p=0 a 1. Luego 1∨q (con q=1) da 1.",
                retro_correcta="¡Bien! ¬p=1, y 1∨1=1.",
            )
            RetoCifrado.objects.create(
                subtema=s2, orden=3, recompensa_exp=70,
                acertijo_logico={"mensaje_cifrado": "p=1, q=0. Calcula (p → q) ∧ (q → p)", "respuesta": "0"},
                pista="Es una bicondicional: solo es verdadera si ambas implicaciones (p→q y q→p) lo son.",
                retro_incorrecta="Con p=1, q=0: p→q es falso (0), así que toda la conjunción ya es falsa (0).",
                retro_correcta="¡Exacto! Basta con que una de las dos implicaciones falle para que sea 0.",
            )

        if not s3.retos.exists():
            RetoDD.objects.create(
                subtema=s3, orden=1, recompensa_exp=30,
                catalogo_dd={"categorias": ["Intersección", "Diferencia", "Unión"],
                             "elementos": ["Diagrama A", "Diagrama B", "Diagrama C"],
                             "solucion": ["Intersección", "Diferencia", "Unión"]},
                pista="Intersección = zona compartida. Diferencia = solo un lado. Unión = todo junto.",
                retro_incorrecta="Revisa: A=Intersección, B=Diferencia, C=Unión.",
                retro_correcta="¡Correcto! Identificaste bien cada tipo de diagrama.",
            )
            RetoDD.objects.create(
                subtema=s3, orden=2, recompensa_exp=50,
                catalogo_dd={"categorias": ["Solo automática", "Ambos", "Solo manual"],
                             "elementos": ["18 personas", "12 personas", "8 personas"],
                             "solucion": ["Solo automática", "Ambos", "Solo manual"]},
                pista="18 solo automático, 12 ambos, 8 solo manual (del ejemplo de la encuesta de coches).",
                retro_incorrecta="18→Solo automática, 12→Ambos, 8→Solo manual.",
                retro_correcta="¡Bien! Así se reparten los 38 encuestados.",
            )
            RetoDecision.objects.create(
                subtema=s3, orden=3, recompensa_exp=70,
                opciones_botones={"pregunta": "¿(A ∪ B)' = A' ∩ B'?",
                                   "opciones": ["Verdadero", "Falso"], "correcta": "Verdadero"},
                pista="Es la Primera Ley de De Morgan, tal como se vio en la teoría.",
                retro_incorrecta="Sí es verdadera: es exactamente la Ley de Unión de De Morgan.",
                retro_correcta="¡Correcto! Esa es la Ley de Unión de De Morgan.",
            )

        if not Alumno.objects.exists():
            alumno = Alumno.objects.create(nombre_alumno="Alumno de Prueba", correo="prueba@recode.com")
            alumno.set_password("test1234")
            alumno.save()
            ProgresoAlumno.objects.create(alumno=alumno)

        self.stdout.write(self.style.SUCCESS("Datos de prueba creados/verificados correctamente."))