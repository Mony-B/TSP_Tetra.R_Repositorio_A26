from django.urls import path

from . import views

app_name = "batalla_final"

urlpatterns = [
    path("", views.jugar, name="jugar"),
    path("iniciar/", views.iniciar, name="iniciar"),
    path("siguiente/", views.siguiente, name="siguiente"),
    path("responder/", views.responder, name="responder"),
    path("tiempo/", views.tiempo_agotado, name="tiempo"),
    path("pausa/", views.pausa, name="pausa"),
    path("abandonar/", views.abandonar, name="abandonar"),
]
