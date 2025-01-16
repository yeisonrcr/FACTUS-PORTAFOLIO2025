# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_repuestos, name='lista_repuestos'),
    path('repuesto/<int:pk>/', views.detalle_repuesto, name='detalle_repuesto'),
    path('repuesto/<int:repuesto_id>/comentario/', views.agregar_comentario, name='agregar_comentario'),
    
    path('categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_por_categoria'),

]


urlpatterns += [
    
    path('ver-mas-especiales/', views.ver_mas_especiales, name='ver_mas_especiales'),


    
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    
    path('carrito/actualizar-cantidad/<int:item_id>', views.actualizar_cantidad, name='actualizar_cantidad'),
    
    path('carrito/agregar/<int:repuesto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/actualizar/<int:item_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path('carrito/eliminar-item/<int:item_id>', views.eliminar_item, name='eliminar_item'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('carrito/pago/', views.procesar_pago, name='procesar_pago'),
    
    path('categories/', views.categoria_lista, name='categorias_lista'),
    


]

