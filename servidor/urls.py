from django.contrib import admin


#configuracion para guardar fotos en el servidor
from django.conf import settings # ingresar a configuracion del setting 
from django.conf.urls.static import static #archivos statics

from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portafolio.urls')), #url apps portafolio
    

    path('accounts/', include('accounts.urls')), #agregamos ambas urls
    path('accounts/', include('django.contrib.auth.urls')), #agregamos urls por defecto para el sistema loginSignup
    #incluyo las vistas predefinidad en django por defecto
    
    
    #urls para la gestion del condominio y guardado de las fotos
    path('condominio/', include('condominio.urls')), #agregamos urls de gestion
    
    
    
    
    #urls para la app de oficiales
    path('oficiales/', include('oficiales.urls')), #agregamos urls de oficiales app
    
    #urls para la app consultas
    path('autopartes/', include('gyna.urls')), #agregamos urls de oficiales app
    
    
    #urls para la app ecommerse
    path('ecom/', include('tiendas.urls')), #agregamos urls de oficiales app
    
    path('blog/', include('blog.urls')), #agregamos urls de oficiales app
    
    
]

#manejo de los archivos staticos MEDIAS IMAGENES
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    