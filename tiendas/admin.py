from django.contrib import admin
from .models import Tienda, Producto, Categoria, Carrito, ItemCarrito, Provincia, Canton,Distrito

@admin.register(Provincia)
class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Canton)
class CantonAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'provincia')
    list_filter = ('provincia',)
    search_fields = ('nombre', 'provincia__nombre')

@admin.register(Distrito)
class DistritoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'canton')
    list_filter = ('canton',)
    search_fields = ('nombre', 'canton__nombre')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug')
    prepopulated_fields = {'slug': ('nombre',)}
    search_fields = ('nombre',)

@admin.register(Tienda)
class TiendaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'propietario', 'provincia', 'canton')
    list_filter = ('provincia', 'canton')
    search_fields = ('nombre', 'propietario__username', 'provincia__nombre', 'canton__nombre')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tienda', 'categoria', 'precio', 'stock')
    list_filter = ('tienda', 'categoria')
    search_fields = ('nombre', 'detalles', 'tienda__nombre')

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tienda')
    list_filter = ('tienda',)
    search_fields = ('usuario__username', 'tienda__nombre')

@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ('carrito', 'producto', 'cantidad', 'precio_unitario', 'subtotal')
    list_filter = ('carrito__tienda', 'producto__categoria')
    search_fields = ('producto__nombre', 'carrito__usuario__username')