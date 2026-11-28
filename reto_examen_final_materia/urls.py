from django.urls import path
from . import views

app_name = "reto_examen_final_materia"

urlpatterns = [
    path("<slug:ejercicio_id>/", views.jugar, name="jugar"),
]
