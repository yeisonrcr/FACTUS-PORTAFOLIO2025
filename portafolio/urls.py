from django.urls import path
from . import views

#agrego los views.py para darles URLs
urlpatterns = [ #ingreso pagina 1 y pagina 2 del portafolio views para direccionar

    path('', views.index, name='paginaUNO'), #pantalla principal de todo el proyecto 
    path('cv/', views.proyecto, name='proyectos'),    #ir a proyectos
]

