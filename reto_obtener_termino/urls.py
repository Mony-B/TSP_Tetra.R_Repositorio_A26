from django.urls import path
from . import views

app_name = "reto_obtener_termino"

urlpatterns = [
    path("<slug:ejercicio_id>/", views.jugar, name="jugar"),
    path("<slug:ejercicio_id>/revisar/", views.revisar, name="revisar"),
    path("<slug:ejercicio_id>/reiniciar/", views.reiniciar, name="reiniciar"),
]
