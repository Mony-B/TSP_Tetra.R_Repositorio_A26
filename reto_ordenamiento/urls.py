from django.urls import path
from . import views

app_name = "reto_ordenamiento"

urlpatterns = [
    path("<slug:ejercicio_id>/", views.jugar, name="jugar"),
    path("<slug:ejercicio_id>/verificar/", views.verificar, name="verificar"),
]
