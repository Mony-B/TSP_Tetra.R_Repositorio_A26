"""
Funciones que usan las demás apps para registrar y consultar el avance.
Así ninguna otra app toca los modelos directamente.
"""
from django.db import IntegrityError, transaction
from django.db.models import F

from .models import Progreso, RetoResuelto, IntentoExamen, NovelaVista


def obtener_progreso(alumno):
    progreso, _ = Progreso.objects.get_or_create(alumno=alumno)
    return progreso


def _sumar_bitcoins(alumno, cantidad):
    if cantidad:
        obtener_progreso(alumno)
        Progreso.objects.filter(alumno=alumno).update(bitcoins=F("bitcoins") + cantidad)


# --- Retos -----------------------------------------------------------------

def reto_resuelto(alumno, reto):
    return RetoResuelto.objects.filter(alumno=alumno, reto=reto).exists()


def retos_resueltos(alumno):
    return set(RetoResuelto.objects.filter(alumno=alumno).values_list("reto", flat=True))


def registrar_reto(alumno, reto, bitcoins):
    """Marca el reto como resuelto. Devuelve los bitcoins otorgados
    (0 si ya lo había resuelto antes)."""
    try:
        with transaction.atomic():
            RetoResuelto.objects.create(alumno=alumno, reto=reto, bitcoins_otorgados=bitcoins)
            _sumar_bitcoins(alumno, bitcoins)
    except IntegrityError:
        return 0
    return bitcoins


# --- Avance dentro de un reto (pasos ya contestados bien) -------------------
# Se guarda en la sesión mientras el alumno juega; al terminar el reto se
# registra en la base de datos con registrar_reto().

def pasos_correctos(request, reto):
    return set(request.session.get(f"reto:{reto}", []))


def marcar_paso(request, reto, paso):
    pasos = pasos_correctos(request, reto)
    pasos.add(paso)
    request.session[f"reto:{reto}"] = sorted(pasos)
    return pasos


def reiniciar_pasos(request, reto):
    request.session.pop(f"reto:{reto}", None)


# --- Exámenes --------------------------------------------------------------

def examen_aprobado(alumno, examen):
    return IntentoExamen.objects.filter(alumno=alumno, examen=examen, aprobado=True).exists()


def examenes_aprobados(alumno):
    return set(
        IntentoExamen.objects.filter(alumno=alumno, aprobado=True).values_list("examen", flat=True)
    )


def registrar_examen(alumno, examen, aciertos, total, aprobado, bitcoins):
    """Guarda el intento. Los bitcoins se dan solo la primera vez que se aprueba."""
    with transaction.atomic():
        otorgados = bitcoins if (aprobado and not examen_aprobado(alumno, examen)) else 0
        IntentoExamen.objects.create(
            alumno=alumno, examen=examen, aciertos=aciertos, total=total,
            aprobado=aprobado, bitcoins_otorgados=otorgados,
        )
        _sumar_bitcoins(alumno, otorgados)
    return otorgados


# --- Novelas -----------------------------------------------------------------

def novelas_vistas(alumno):
    return set(NovelaVista.objects.filter(alumno=alumno).values_list("materia", flat=True))


def marcar_novela_vista(alumno, materia):
    NovelaVista.objects.get_or_create(alumno=alumno, materia=materia)


# --- Resumen (Mi Perfil y API) ---------------------------------------------

def resumen(alumno):
    return {
        "nombre": alumno.username,
        "bitcoins": obtener_progreso(alumno).bitcoins,
        "retos_resueltos": sorted(retos_resueltos(alumno)),
        "examenes_aprobados": sorted(examenes_aprobados(alumno)),
        "novelas_vistas": sorted(novelas_vistas(alumno)),
    }


# --- Respuesta común para las apps de reto ------------------------------------

def procesar_paso(request, reto, paso, correcto, total_pasos, bitcoins):
    """Cada app de reto revisa la respuesta con su propia lógica y luego llama
    a esta función. Lleva la cuenta de pasos correctos y, cuando están todos,
    registra el reto (bitcoins solo la primera vez).

    Devuelve el diccionario que la app regresa como JSON al navegador.
    """
    alumno = request.user
    datos = {"correcto": correcto, "completado": False, "bitcoins_otorgados": 0}
    if correcto:
        pasos = marcar_paso(request, reto, paso)
        datos["pasos_correctos"] = len(pasos)
        if len(pasos) >= total_pasos:
            datos["completado"] = True
            datos["bitcoins_otorgados"] = registrar_reto(alumno, reto, bitcoins)
            reiniciar_pasos(request, reto)
    datos["bitcoins_total"] = obtener_progreso(alumno).bitcoins
    return datos
