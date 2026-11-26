from django.urls import path
from . import views

app_name = "reto_parabolica"

urlpatterns = [
    path("<slug:ejercicio_id>/", views.jugar, name="jugar"),
    path("<slug:ejercicio_id>/disparo/", views.disparo, name="disparo"),
    path("<slug:ejercicio_id>/reintentar/", views.reintentar, name="reintentar"),
]
