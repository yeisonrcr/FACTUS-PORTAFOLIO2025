from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_facturas, name='lista_facturas'),
    path('crear/', views.crear_factura, name='crear_factura'),
    path('validar/<int:factura_id>/', views.validar_factura, name='validar_factura'),
    path('factura/<int:factura_id>/detalles/', views.lista_detalles_factura, name='lista_detalles_factura'),
    path('factura/<int:factura_id>/detalles/crear/', views.crear_detalle_factura, name='crear_detalle_factura'),
    path('detalle/<int:detalle_id>/editar/', views.editar_detalle_factura, name='editar_detalle_factura'),
    path('detalle/<int:detalle_id>/eliminar/', views.eliminar_detalle_factura, name='eliminar_detalle_factura'),
]
