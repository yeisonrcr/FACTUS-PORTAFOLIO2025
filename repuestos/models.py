from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image

class Marca(models.Model):
    """
    Modelo que representa una marca de autos.
    """
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class AnioAuto(models.Model):
    """
    Modelo que representa un año de un auto.
    """
    anio = models.IntegerField(help_text="Ejemplo: 2015", unique=True)

    def __str__(self):
        return str(self.anio)

class Modelo(models.Model):
    """
    Modelo que representa un modelo de auto.
    """
    nombre = models.CharField(max_length=100)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='modelos')
    
    def __str__(self):
        return f"{self.marca} - {self.nombre}"

class ModeloAnio(models.Model):
    """
    Modelo intermedio que relaciona modelos de autos con años.
    """
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE, related_name='modelos_anio')
    anios = models.ManyToManyField(AnioAuto, related_name='modelos_anio')
    
    def __str__(self):
        anios = ', '.join(str(anio.anio) for anio in self.anios.all())
        return f"{self.modelo} - Años compatibles: {anios}"

class Categoria(models.Model):
    """
    Modelo que representa una categoría de repuestos.
    """
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre



class Repuesto(models.Model):
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=200, null=True, blank=True)
    descripcion = models.TextField()
    categorias = models.ManyToManyField(Categoria, related_name='repuestos_categoria')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    modelos_anios_compatibles = models.ManyToManyField(ModeloAnio, related_name='repuestos')
    en_oferta = models.BooleanField(default=False)
    oferta_especial = models.BooleanField(default=False)
    porcentaje_descuento = models.DecimalField(
        max_digits=5, 
        decimal_places=0,
        default=0,
        help_text="Porcentaje de descuento actual del producto"
    )

    def imagen_principal(self):
        return self.imagenes.filter(es_principal=True).first()

    def tiene_imagenes_requeridas(self):
        return self.imagenes.count() >= 1

    def promedio_calificacion(self):
        calificaciones = self.comentarios.all().values_list('calificacion', flat=True)
        if calificaciones:
            return sum(calificaciones) / len(calificaciones)
        return 0

    def calcular_precio_con_descuento(self):
        """
        Calcula el precio con descuento basado en el porcentaje
        """
        if self.oferta_especial and self.porcentaje_descuento > 0:
            descuento = self.precio * (self.porcentaje_descuento / Decimal('100'))
            return self.precio - descuento
        
        if self.en_oferta and self.porcentaje_descuento > 0:
            descuento = self.precio * (self.porcentaje_descuento / Decimal('100'))
            return self.precio - descuento
        return self.precio

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre



class ImagenRepuesto(models.Model):
    """
    Modelo que representa una imagen de un repuesto.
    """
    repuesto = models.ForeignKey(Repuesto, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='repuestos/')
    es_principal = models.BooleanField(default=False)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden']
        verbose_name = "Imagen"
        verbose_name_plural = "Imágenes"

    def __str__(self):
        return f"Imagen {self.orden} de {self.repuesto.nombre}"
    
    def save(self, *args, **kwargs):
        """
        Guarda la imagen y ajusta el tamaño de la misma.
        """
        super().save(*args, **kwargs)
        if self.imagen:
            img = Image.open(self.imagen.path)
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.imagen.path)

class Comentario(models.Model):
    """
    Modelo que representa un comentario sobre un repuesto.
    """
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    calificacion = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['repuesto', 'usuario']  # Un usuario solo puede comentar una vez por repuesto

    def __str__(self):
        return f"Comentario de {self.usuario} en {self.repuesto}"

class Carrito(models.Model):
    """
    Modelo que representa el carrito de compras de un usuario.
    """
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='carrito')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def total(self):
        """
        Calcula el total del carrito sumando los subtotales de los items.
        """
        return sum(item.subtotal() for item in self.items.all())

    def cantidad_items(self):
        """
        Calcula la cantidad de items en el carrito.
        """
        return self.items.count()

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

class ItemCarrito(models.Model):
    """
    Modelo que representa un item en el carrito de compras.
    """
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        """
        Calcula el subtotal del item en el carrito.
        """
        return self.repuesto.calcular_precio_con_descuento() * self.cantidad

    class Meta:
        unique_together = ['carrito', 'repuesto']

    def __str__(self):
        return f"{self.cantidad} x {self.repuesto.nombre}"

class Orden(models.Model):
    """
    Modelo que representa una orden de compra.
    """
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Orden {self.id} - {self.usuario.username}"

class ItemOrden(models.Model):
    """
    Modelo que representa un item en una orden de compra.
    """
    orden = models.ForeignKey(Orden, related_name='items', on_delete=models.CASCADE)
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.cantidad} x {self.repuesto.nombre} en Orden {self.orden.id}"

    def save(self, *args, **kwargs):
        """
        Calcula el subtotal del item en la orden y lo guarda.
        """
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
