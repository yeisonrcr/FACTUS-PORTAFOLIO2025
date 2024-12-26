from django.urls import path
from . import views


urlpatterns = [ 
    path('', views.todo, name='todo_oficial'),
    #path('visitas-autorizadas/', views.visitas_Autorizadas, name='autorizados_oficial'),
    #path('permanentes', views.permanentes, name='permanentes_oficial'),
    #path('mascotas', views.mascotas_condominio, name='mascotas_oficial'),
    #path('autos', views.auto_condominio, name='autos_oficial'),
    
]

