from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_temas, name="lista_temas"),
    path("tema/<int:tema_id>/", views.lista_subtemas, name="lista_subtemas"),
    path("subtema/<int:subtema_id>/", views.seleccion_retos, name="seleccion_retos"),
    path("reto/<int:reto_id>/", views.resolver_reto, name="resolver_reto"),
    path("tema/<int:tema_id>/examen/", views.contestar_examen, name="contestar_examen"),
]