from django.urls import path
from . import views

app_name = "mapa"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("materia/<slug:slug>/", views.materia, name="materia"),
]
