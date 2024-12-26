from django.db import models
import re
from unidecode import unidecode

class Blog(models.Model):
    # Título del blog, este será usado solo para el título visible
    titulo_blog = models.CharField(max_length=255, unique=True)
    
    categoria= models.CharField(max_length=255,null=True, blank=True)

    # Slug del blog, este se utilizará para la URL
    slug_blog = models.SlugField(max_length=255, unique=True, blank=True)
    

    # Resumen breve del blog
    resumen_blog = models.TextField(blank=False, null=False)

    # Características o etiquetas del blog
    caracteristica_blog = models.TextField(blank=False, null=False)

    # Explicación más detallada del blog
    explicacion_blog = models.TextField(blank=False, null=False)

    # URL de YouTube asociada al blog (si existe)
    youtube_blog = models.CharField(max_length=100, null=True, blank=True)

    # Código del blog
    codigo_blog = models.TextField(blank=True, null=True)

    # Fecha de creación (solo se asigna al momento de crear el objeto)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # Imagen asociada al blog
    imagen_blog = models.ImageField(upload_to='blogs/', null=True, blank=True)

    # Método save para personalizar el guardado
    def save(self, *args, **kwargs):
        """
        Personaliza el guardado del objeto Blog.
        Si no tiene slug (slug_blog), lo generamos automáticamente
        basado en 'titulo_blog'.
        """
        # Generar el slug si está vacío 
        if not self.slug_blog:
            # Usamos el título para crear un slug amigable
            slug = self.titulo_blog.lower().replace(' ', '-')
            # Eliminar tildes o acentos usando unidecode
            slug = unidecode(slug)
            
            # Limitar la longitud del slug a 255 caracteres (máximo permitido por el SlugField)
            slug = slug[:255]
            
            # Eliminar caracteres no permitidos en una URL (como acentos o símbolos)
            slug = re.sub(r'[^\w\s-]', '', slug)
            
            # Reemplazar múltiples guiones por uno solo
            slug = re.sub(r'[-\s]+', '-', slug)
            
            # Asignamos el slug generado al campo slug_blog
            self.slug_blog = slug
        
        # Llamamos al método save del modelo padre para realizar el guardado
        super().save(*args, **kwargs)

    def __str__(self):
        # Representación en cadena del objeto, mostrando el título del blog
        return self.titulo_blog
