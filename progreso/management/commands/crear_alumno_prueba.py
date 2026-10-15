from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from progreso.servicios import obtener_progreso


class Command(BaseCommand):
    help = "Crea el alumno de prueba (usuario: prueba, contraseña: test1234) si no existe"

    def handle(self, *args, **options):
        User = get_user_model()
        alumno, creado = User.objects.get_or_create(username="prueba")
        if creado:
            alumno.set_password("test1234")
            alumno.save()
        obtener_progreso(alumno)
        self.stdout.write(self.style.SUCCESS("Alumno de prueba listo (prueba / test1234)."))
