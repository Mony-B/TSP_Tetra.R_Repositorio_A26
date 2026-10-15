from django.contrib import admin
from .models import Progreso, RetoResuelto, IntentoExamen, NovelaVista


@admin.register(Progreso)
class ProgresoAdmin(admin.ModelAdmin):
    list_display = ("alumno", "bitcoins")


@admin.register(RetoResuelto)
class RetoResueltoAdmin(admin.ModelAdmin):
    list_display = ("alumno", "reto", "bitcoins_otorgados", "fecha")
    list_filter = ("reto",)


@admin.register(IntentoExamen)
class IntentoExamenAdmin(admin.ModelAdmin):
    list_display = ("alumno", "examen", "aciertos", "total", "aprobado", "fecha")
    list_filter = ("examen", "aprobado")


admin.site.register(NovelaVista)
