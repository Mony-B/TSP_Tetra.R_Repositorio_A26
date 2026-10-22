from django.urls import path
from . import views

app_name = "reto_clasificar"

urlpatterns = [
    path("<slug:ejercicio_id>/", views.jugar, name="jugar"),
    path("<slug:ejercicio_id>/clasificar/", views.clasificar, name="clasificar"),
    path("<slug:ejercicio_id>/completar/", views.completar, name="completar"),
]