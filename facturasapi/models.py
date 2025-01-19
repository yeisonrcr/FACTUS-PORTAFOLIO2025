from django.db import models  # Importar módulos de modelos de Django
from django.utils import timezone  # Importar utilidades de zona horaria de Django

class Cliente(models.Model):
    nit = models.CharField(max_length=20)  # Campo para el NIT del cliente
    dv = models.CharField(max_length=1, null=True, blank=True)  # Dígito de verificación (opcional)
    razon_social = models.CharField(max_length=200)  # Campo para la razón social del cliente
    direccion = models.CharField(max_length=200)  # Dirección del cliente
    email = models.EmailField()  # Correo electrónico del cliente
    telefono = models.CharField(max_length=20)  # Teléfono del cliente
    municipio_id = models.CharField(max_length=10, default="980")  # ID del municipio según Factus
    created_at = models.DateTimeField(default=timezone.now)  # Fecha y hora de creación del registro

    def __str__(self):
        return f"{self.razon_social} - {self.nit}"  # Representación en cadena del objeto Cliente


class Facturax(models.Model):
    ESTADO_CHOICES = [
        ('CREADA', 'Creada'),  # Factura creada
        ('VALIDADA', 'Validada'),  # Factura validada
        ('ENVIADA', 'Enviada a DIAN'),  # Factura enviada a DIAN
        ('ERROR', 'Error'),  # Error en la factura
    ]

    numero_factura = models.CharField(max_length=50, unique=True)  # Número único de la factura
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Referencia al cliente asociado
    fecha_emision = models.DateTimeField(default=timezone.now)  # Fecha de emisión de la factura
    fecha_vencimiento = models.DateField(null=True, blank=True)  # Fecha de vencimiento de la factura (opcional)
    
    forma_pago = models.CharField(max_length=2, default="1")  # Forma de pago: 1=contado, 2=crédito
    metodo_pago = models.CharField(max_length=2, default="10")  # Método de pago: 10=efectivo
    observacion = models.CharField(max_length=250, blank=True)  # Observaciones (opcional)
    valor_total = models.DecimalField(max_digits=15, decimal_places=2)  # Valor total de la factura
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='CREADA')  # Estado de la factura
    respuesta_dian = models.JSONField(null=True, blank=True)  # Respuesta de DIAN (opcional)
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha y hora de creación del registro
    updated_at = models.DateTimeField(auto_now=True)  # Fecha y hora de la última actualización del registro

    def __str__(self):
        return f"Factura {self.numero_factura} - {self.cliente.razon_social}"  # Representación en cadena del objeto Facturax


class DetalleFactura(models.Model):
    factura = models.ForeignKey(Facturax, related_name='detalles', on_delete=models.CASCADE)  # Referencia a la factura asociada
    codigo_referencia = models.CharField(max_length=50)  # Código de referencia del producto/servicio
    descripcion = models.CharField(max_length=200)  # Descripción del producto/servicio
    cantidad = models.IntegerField()  # Cantidad del producto/servicio
    valor_unitario = models.DecimalField(max_digits=15, decimal_places=2)  # Valor unitario del producto/servicio
    tasa_impuesto = models.DecimalField(max_digits=5, decimal_places=2, default=19.00)  # Tasa de impuesto (%)
    tasa_descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Tasa de descuento (%)
    unidad_medida_id = models.IntegerField(default=70)  # ID de la unidad de medida según Factus
    tributo_id = models.IntegerField(default=1)  # ID del tributo según Factus
    valor_total = models.DecimalField(max_digits=15, decimal_places=2)  # Valor total del detalle de factura
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha y hora de creación del registro

    def save(self, *args, **kwargs):
        # Calcula el valor total incluyendo impuestos y descuentos
        valor_sin_descuento = float(self.cantidad) * float(self.valor_unitario)  # Calcular valor sin descuento
        descuento = valor_sin_descuento * (float(self.tasa_descuento) / 100)  # Calcular descuento
        valor_con_descuento = valor_sin_descuento - descuento  # Calcular valor con descuento
        impuesto = valor_con_descuento * (float(self.tasa_impuesto) / 100)  # Calcular impuesto
        self.valor_total = valor_con_descuento + impuesto  # Calcular valor total
        super().save(*args, **kwargs)  # Llamar al método save del modelo base

    def __str__(self):
        return f"{self.descripcion} - {self.factura.numero_factura}"  # Representación en cadena del objeto DetalleFactura
