from django.urls import path
from . import views

#agrego los views.py para darles URLs
urlpatterns = [ #ingreso pagina 1 y pagina 2 del portafolio views para direccionar

    path('', views.blog, name='blog'),
    
    
    
    
    
    
    
    
    
    
    
    # Ruta para mostrar toda la información del blog
    
    # path('blog/<slug:slug>/', views.detalle_blog, name='detalle_blog'),  
    # #vamos a mostrar unicamente todos los Blogs registrados sin ver o editarlos, más adelante pero dejamos el url por slug listo 
    
    
]

