"""
Único componente con modelos. Guarda el avance del alumno.

El alumno es el User de Django (tabla auth_user), así que aquí solo se
guarda lo que es propio del juego. Los retos, exámenes y materias se
identifican por texto (ej. "reto_ecuaciones:basicas", "logica"), porque su
contenido vive en el código de cada app y no en la base de datos.
"""
from django.conf import settings
from django.db import models


class Progreso(models.Model):
    alumno = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="progreso"
    )
    bitcoins = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "progresos"

    def __str__(self):
        return f"Progreso de {self.alumno.username}"


class RetoResuelto(models.Model):
    alumno = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="retos_resueltos"
    )
    reto = models.CharField(max_length=100, help_text='"app:ejercicio", ej. reto_ecuaciones:basicas')
    bitcoins_otorgados = models.PositiveIntegerField(default=0)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "retos resueltos"
        # Un registro por reto: los bitcoins se dan solo la primera vez.
        constraints = [
            models.UniqueConstraint(fields=["alumno", "reto"], name="reto_resuelto_una_vez"),
        ]

    def __str__(self):
        return f"{self.alumno.username} - {self.reto}"


class IntentoExamen(models.Model):
    alumno = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="intentos_examen"
    )
    examen = models.CharField(max_length=50, help_text='materia o "final"')
    aciertos = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    aprobado = models.BooleanField(default=False)
    bitcoins_otorgados = models.PositiveIntegerField(default=0)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "intentos de examen"
        ordering = ["-fecha"]

    def __str__(self):
        estado = "aprobado" if self.aprobado else "reprobado"
        return f"{self.alumno.username} - {self.examen} ({self.aciertos}/{self.total}, {estado})"


class NovelaVista(models.Model):
    alumno = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="novelas_vistas"
    )
    materia = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "novelas vistas"
        constraints = [
            models.UniqueConstraint(fields=["alumno", "materia"], name="novela_vista_una_vez"),
        ]

    def __str__(self):
        return f"{self.alumno.username} vio {self.materia}"
