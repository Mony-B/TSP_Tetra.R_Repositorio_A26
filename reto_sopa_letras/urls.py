from django.urls import path
from . import views

app_name = "reto_sopa_letras"

urlpatterns = [
    path("<slug:ejercicio_id>/", views.jugar, name="jugar"),
    path("<slug:ejercicio_id>/revisar/", views.revisar, name="revisar"),
]
