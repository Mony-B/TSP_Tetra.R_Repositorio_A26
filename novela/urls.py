from django.urls import path
from . import views

app_name = "novela"

urlpatterns = [
    path("<slug:slug>/", views.ver, name="ver"),
    path("<slug:slug>/saltar/", views.saltar, name="saltar"),
]
