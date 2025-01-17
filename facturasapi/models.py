from django.db import models
from django.utils import timezone

class Cliente(models.Model):
    nit = models.CharField(max_length=20)
    dv = models.CharField(max_length=1, null=True, blank=True)  # Dígito de verificación
    razon_social = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    municipio_id = models.CharField(max_length=10, default="980")  # ID del municipio según Factus
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.razon_social} - {self.nit}"

class DetalleFactura(models.Model):
    factura = models.ForeignKey('Factura', related_name='detalles', on_delete=models.CASCADE)
    codigo_referencia = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    cantidad = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=15, decimal_places=2)
    tasa_impuesto = models.DecimalField(max_digits=5, decimal_places=2, default=19.00)
    tasa_descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    unidad_medida_id = models.IntegerField(default=70)
    tributo_id = models.IntegerField(default=1)
    valor_total = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calcula el valor total incluyendo impuestos y descuentos
        valor_sin_descuento = float(self.cantidad) * float(self.valor_unitario)
        descuento = valor_sin_descuento * (float(self.tasa_descuento) / 100)
        valor_con_descuento = valor_sin_descuento - descuento
        impuesto = valor_con_descuento * (float(self.tasa_impuesto) / 100)
        self.valor_total = valor_con_descuento + impuesto
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.descripcion} - {self.factura.numero_factura}"

class Factura(models.Model):
    ESTADO_CHOICES = [
        ('CREADA', 'Creada'),
        ('VALIDADA', 'Validada'),
        ('ENVIADA', 'Enviada a DIAN'),
        ('ERROR', 'Error'),
    ]

    numero_factura = models.CharField(max_length=50, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_emision = models.DateTimeField(default=timezone.now)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    forma_pago = models.CharField(max_length=2, default="1")  # 1=contado, 2=crédito
    metodo_pago = models.CharField(max_length=2, default="10")  # 10=efectivo
    observacion = models.CharField(max_length=250, blank=True)
    valor_total = models.DecimalField(max_digits=15, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='CREADA')
    respuesta_dian = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Factura {self.numero_factura} - {self.cliente.razon_social}"