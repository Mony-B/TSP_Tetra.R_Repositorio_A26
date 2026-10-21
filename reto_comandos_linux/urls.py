from django.urls import path
from . import views

app_name = "reto_comandos_linux"

urlpatterns = [
    path("<slug:ejercicio_id>/", views.jugar, name="jugar"),
    path("<slug:ejercicio_id>/comando/", views.comando, name="comando"),
    path("<slug:ejercicio_id>/puerta/", views.puerta, name="puerta"),
]
