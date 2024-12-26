from django.contrib import admin
from .models import Blog
from .forms import BlogForm  # Importar el formulario personalizado


class BlogAdmin(admin.ModelAdmin):
    # Usar el formulario personalizado en el admin
    form = BlogForm

    # Campos que se mostrarán en la lista de blogs
    list_display = ('titulo_blog', 'slug_blog', 'fecha_creacion')

    # Campos que serán editables desde la lista
    list_editable = ('slug_blog',)

    # Organización de los campos en el formulario del admin
    fieldsets = (
        (None, {
            'fields': ('titulo_blog', 'slug_blog', 'resumen_blog', 'caracteristica_blog', 'explicacion_blog', 'youtube_blog', 'codigo_blog')
        }),
        ('Imagen', {
            'fields': ('imagen_blog',)
        }),
        ('Fechas', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',),  # Ocultar el panel de fechas por defecto
        }),
    )

    # Aseguramos que solo los campos necesarios sean mostrados
    readonly_fields = ('fecha_creacion',)

    # Habilitamos la búsqueda por título del blog, slug y resumen
    search_fields = ('titulo_blog', 'slug_blog', 'resumen_blog')

    # Filtro por fecha de creación y título
    list_filter = ('fecha_creacion',)

    # Ordenar por fecha de creación de forma descendente
    ordering = ('-fecha_creacion',)

    # No es necesario pre-poblar el campo slug_blog ya que se maneja en el formulario
    # prepopulated_fields = {'slug_blog': ('titulo_blog',)}

# Registrar el modelo con el admin personalizado
admin.site.register(Blog, BlogAdmin)
