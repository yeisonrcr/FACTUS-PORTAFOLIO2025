from django.urls import path

from django.contrib.auth import views as logged
from . import views

urlpatterns = [
    path('logout/', logged.LogoutView.as_view(), name="logout" ), 
    path('signup/', views.crear_cuenta, name="signup" ), #asignamos el controlador a una url para acceder a crear la cuenta 
    path('', views.inicio, name="home" ) #esta pagina no se utilizará solo para el testing
]
