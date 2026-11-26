from django.urls import path

from . import views

app_name = "red_corrupta"

urlpatterns = [
    path("", views.catalogo, name="catalogo"),
    path("<str:pista_id>/comprar/", views.comprar, name="comprar"),
    path("<str:pista_id>/snake-completado/", views.snake_completado, name="snake_completado"),
]
