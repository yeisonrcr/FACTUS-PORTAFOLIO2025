from django.urls import path
from . import views



#urls de gestion de condominio
urlpatterns = [
    #URLs HOME
    
    path('home/', views.home, name='condominio_home'),
    
    
    
    #se utiliza el ORM de DJANGO en esta aplicacion
    
    # URLs para manejar los permanentes del usuario en el condominio
    path('lista_permanentes/', views.perfil_usuario_lista, name='perfil_usuario_lista'),
    path('detalle_permanente/<int:pk>', views.perfil_usuario_detalle, name='perfil_usuario_detalle'),
    path('nuevo_permanente/nuevo/', views.perfil_usuario_nuevo, name='perfil_usuario_nuevo'),
    path('perfil_permanente/<int:pk>/editar/', views.perfil_usuario_editar, name='perfil_usuario_editar'),
    path('perfil_permanente/<int:pk>/eliminar/', views.perfil_usuario_eliminar, name='perfil_usuario_eliminar'),
    

    # URLs para manejar las visitas diarias del usuario en el condominio / oficiales de seguridad APIREST
    path('registro_visitas/', views.registro_visitas_lista, name='registro_visitas_lista'),
    path('registro_visitas/<int:pk>/', views.registro_visitas_detalle, name='registro_visitas_detalle'),
    path('registro_visitas/nuevo/', views.registro_visitas_nuevo, name='registro_visitas_nuevo'),
    path('registro_visitas/<int:pk>/editar/', views.registro_visitas_editar, name='registro_visitas_editar'),
    path('registro_visitas/<int:pk>/eliminar/', views.registro_visitas_eliminar, name='registro_visitas_eliminar'),

    # URLs para RegistroAutomoviles del usuario en el condominio / oficiales de seguridad APIREST
    path('registro_automoviles/', views.registro_automoviles_lista, name='registro_automoviles_lista'),
    path('registro_automoviles/<int:pk>/', views.registro_automoviles_detalle, name='registro_automoviles_detalle'),
    path('registro_automoviles/nuevo/', views.registro_automoviles_nuevo, name='registro_automoviles_nuevo'),
    path('registro_automoviles/<int:pk>/editar/', views.registro_automoviles_editar, name='registro_automoviles_editar'),
    path('registro_automoviles/<int:pk>/eliminar/', views.registro_automoviles_eliminar, name='registro_automoviles_eliminar'),

    # URLs para RegistroMascotas del usuario en el condominio / oficiales de seguridad APIREST
    path('registro_mascotas/', views.registro_mascotas_lista, name='registro_mascotas_lista'),
    path('registro_mascotas/<int:pk>/', views.registro_mascotas_detalle, name='registro_mascotas_detalle'),
    path('registro_mascotas/nuevo/', views.registro_mascotas_nuevo, name='registro_mascotas_nuevo'),
    path('registro_mascotas/<int:pk>/editar/', views.registro_mascotas_editar, name='registro_mascotas_editar'),
    path('registro_mascotas/<int:pk>/eliminar/', views.registro_mascotas_eliminar, name='registro_mascotas_eliminar'),
    
    
    # URLs para los reportes
    path('reportes_lista/', views.registro_reporte_lista, name='reportes_lista'),
    path('reporte_detalle/<int:pk>/', views.registro_reporte_detalle, name='reporte_detalle'),
    path('reporte_nuevo/nuevo/', views.registro_reporte_nuevo, name='reporte_nuevo'),
    path('reporte_editar/<int:pk>/editar/', views.registro_reporte_editar, name='reporte_editar'),
    path('reporte_eliminar/<int:pk>/eliminar/', views.registro_reporte_eliminar, name='reporte_eliminar'),
    

    
    
]


