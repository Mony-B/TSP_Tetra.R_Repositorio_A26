from django.urls import path
from . import views

app_name = "progreso"

urlpatterns = [
    path("registro/", views.registro, name="registro"),
    path("perfil/", views.perfil, name="perfil"),
    path("api/", views.api_avance, name="api_avance"),
    path("api/novela/<slug:materia>/vista/", views.api_novela_vista, name="api_novela_vista"),
]
