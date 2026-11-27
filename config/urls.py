from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),

    # Inicio y cierre de sesión con las vistas que ya trae Django
    # (el alumno es el User de Django; el template está en comun).
    path('entrar/', auth_views.LoginView.as_view(), name='login'),
    path('salir/', auth_views.LogoutView.as_view(), name='logout'),

    path('', include('mapa.urls')),
    path('progreso/', include('progreso.urls')),
    path('novela/', include('novela.urls')),
    path('batalla/', include('batalla.urls')),
    path('red-corrupta/', include('red_corrupta.urls')),
    path('retos/algebra-booleana/', include('reto_algebra_booleana.urls')),
    path('retos/comandos-linux/', include('reto_comandos_linux.urls')),
    path('retos/ecuaciones/', include('reto_ecuaciones.urls')),
    path('retos/clasificar/', include('reto_clasificar.urls')),
    path('retos/obtener-termino/', include('reto_obtener_termino.urls')),
    path('retos/sopa-letras/', include('reto_sopa_letras.urls')),
    path('retos/ordenamiento/', include('reto_ordenamiento.urls')),
    path('retos/parabolica/', include('reto_parabolica.urls')),
    path('retos/conceptos/', include('reto_conceptos.urls')),
    path('retos/laberinto/', include('reto_laberinto.urls')),
    path("batalla-final/", include("batalla_final.urls")),
]
