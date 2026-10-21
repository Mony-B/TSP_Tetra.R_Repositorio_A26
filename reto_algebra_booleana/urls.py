from django.urls import path
from . import views

app_name = "reto_algebra_booleana"

urlpatterns = [
    path("<slug:ejercicio_id>/", views.jugar, name="jugar"),
    path("<slug:ejercicio_id>/revisar/", views.revisar, name="revisar"),
]
