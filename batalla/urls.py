from django.urls import path
from . import views

app_name = "batalla"

urlpatterns = [
    path("<slug:slug>/", views.examen, name="examen"),
]
