from .forms import ModeloAnioForm
from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import (
    Marca, Modelo, Repuesto, Comentario, Carrito, 
    ItemCarrito, Categoria, AnioAuto, Orden, ImagenRepuesto, ItemOrden, ModeloAnio
)



# Inlines
class ImagenRepuestoInline(admin.TabularInline):
    """
    Permite agregar imágenes relacionadas con los repuestos en el admin.
    """
    model = ImagenRepuesto
    extra = 1  # Cantidad extra de formularios vacíos
    min_num = 1  # Mínimo número de imágenes
    max_num = 3  # Máximo número de imágenes

class ModeloInline(admin.TabularInline):
    """
    Permite agregar modelos relacionados con las marcas en el admin.
    """
    model = Modelo
    extra = 1

class ItemCarritoInline(admin.TabularInline):
    """
    Permite agregar items relacionados con los carritos en el admin.
    """
    model = ItemCarrito
    extra = 1

class ItemOrdenInline(admin.TabularInline):
    """
    Permite agregar items relacionados con las órdenes en el admin.
    """
    model = ItemOrden
    extra = 1


# Administración de Repuestos
@admin.register(Repuesto)
class RepuestoAdmin(admin.ModelAdmin):
    inlines = [ImagenRepuestoInline]  # Inlines para agregar imágenes
    list_display = ('nombre', 'codigo', 'precio', 'stock', 'fecha_creacion')  # Campos a mostrar
    list_filter = ['categorias', 'modelos_anios_compatibles']  # Filtros
    search_fields = ['nombre', 'codigo', 'descripcion']  # Campos para búsqueda
    filter_horizontal = ['categorias', 'modelos_anios_compatibles']  # Filtros horizontales

    def get_form(self, request, obj=None, **kwargs):
        """
        Valida que el repuesto tenga al menos una imagen.
        """
        form = super().get_form(request, obj, **kwargs)
        if obj and not obj.imagenes.exists():
            self.message_user(request, "Este producto no tiene imágenes. Por favor, agregue al menos una.", level='WARNING')
        return form











# Administración de Años de Auto
@admin.register(AnioAuto)
class AnioAutoAdmin(admin.ModelAdmin):
    list_display = ('anio',)  # Campos a mostrar
    search_fields = ('anio',)  # Campos para búsqueda

# Administración de Modelos
@admin.register(Modelo)
class ModeloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca')  # Campos a mostrar
    search_fields = ('nombre', 'marca__nombre')  # Campos para búsqueda

# Administración de Modelos con Años
@admin.register(ModeloAnio)
class ModeloAnioAdmin(admin.ModelAdmin):
    form = ModeloAnioForm  # Usar el formulario personalizado
    list_display = ('modelo', 'get_anios')  # Campos a mostrar
    search_fields = ('modelo__nombre', 'anios__anio')  # Campos para búsqueda

    def get_anios(self, obj):
        """
        Obtiene los años compatibles para un modelo.
        """
        return ", ".join(str(anio.anio) for anio in obj.anios.all().order_by('anio'))
    get_anios.short_description = 'Años Compatibles'

# Administración de Marcas
admin.site.register(Marca)

# Administración de Órdenes
@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_compra', 'total')  # Campos a mostrar
    search_fields = ('usuario__username',)  # Campos para búsqueda
    inlines = [ItemOrdenInline]  # Inlines para agregar items de órdenes

# Administración de Comentarios
@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('repuesto', 'usuario', 'calificacion', 'fecha')  # Campos a mostrar
    list_filter = ('repuesto', 'calificacion', 'fecha')  # Filtros
    search_fields = ('usuario__username', 'texto')  # Campos para búsqueda

# Administración de Carritos
@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_creacion', 'activo')  # Campos a mostrar
    inlines = [ItemCarritoInline]  # Inlines para agregar items de carritos

# Registrar modelos simples
admin.site.register(ItemCarrito)
admin.site.register(Categoria)
