from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from . import servicios


def registro(request):
    """El alumno crea su cuenta (usuario y contraseña) y se le crea su progreso."""
    if request.user.is_authenticated:
        return redirect("mapa:inicio")
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        alumno = form.save()
        servicios.obtener_progreso(alumno)
        login(request, alumno)
        return redirect("mapa:inicio")
    return render(request, "progreso/registro.html", {"form": form})


@login_required
def perfil(request):
    """Mi Perfil: nombre, avance y bitcoins actuales."""
    from mapa.temas import MATERIAS, retos_de_materia

    datos = servicios.resumen(request.user)
    resueltos = set(datos["retos_resueltos"])
    materias = []
    for materia in MATERIAS:
        retos = retos_de_materia(materia)
        materias.append({
            "nombre": materia["nombre"],
            "resueltos": sum(1 for r in retos if r["clave"] in resueltos),
            "total": len(retos),
            "examen_aprobado": materia["slug"] in datos["examenes_aprobados"],
        })
    return render(request, "progreso/perfil.html", {"datos": datos, "materias": materias})


@login_required
def api_avance(request):
    """API JSON con el avance del alumno (la usa la novela, por ejemplo)."""
    return JsonResponse(servicios.resumen(request.user))


@login_required
@require_POST
def api_novela_vista(request, materia):
    servicios.marcar_novela_vista(request.user, materia)
    return JsonResponse({"ok": True})
