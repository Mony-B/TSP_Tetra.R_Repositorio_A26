from django.contrib import admin
from .models import (
    Ruta, Subtema,
    Alumno, ProgresoAlumno,
    Reto, RetoDD, RetoDecision, RetoCifrado, RetoCF, ResolverReto,
    Examen, ResolverExamen,
    Pista, ComprarPista,
    Recompensa, ReclamarRecompensa,
)

admin.site.register(Ruta)
admin.site.register(Subtema)
admin.site.register(Alumno)
admin.site.register(ProgresoAlumno)
admin.site.register(Reto)
admin.site.register(RetoDD)
admin.site.register(RetoDecision)
admin.site.register(RetoCifrado)
admin.site.register(RetoCF)
admin.site.register(ResolverReto)
admin.site.register(Examen)
admin.site.register(ResolverExamen)
admin.site.register(Pista)
admin.site.register(ComprarPista)
admin.site.register(Recompensa)
admin.site.register(ReclamarRecompensa)