from django.db import models
from django.core.exceptions import ValidationError

# Validador personalizado para asegurar que el valor sea un entero positivo mayor o igual a 5
def validate_positive_integer(value):
    if not isinstance(value, int) or value < 5:
        raise ValidationError("El valor debe ser un número entero positivo.")

# Modelo principal que representa una solicitud
class Request(models.Model):
    # Campos relacionados con la información del vehículo
    tipo = models.CharField(blank=True, max_length=40, null=True)  # Tipo de solicitud
    vehicle_no = models.CharField(blank=True, max_length=17, null=True)  # Número de identificación del vehículo
    vehicle_name = models.CharField(blank=True, max_length=50, null=True)  # Nombre del vehículo
    vehicle_model = models.CharField(blank=True, max_length=40, null=True)  # Modelo del vehículo
    vehicle_brand = models.CharField(blank=True, max_length=15, null=True)  # Marca del vehículo
    
    # Información del cliente
    vehicle_cliente = models.CharField(blank=True, max_length=80, null=True)  # Nombre del cliente
    vehicle_mobile = models.CharField(max_length=15, null=True, blank=True)  # Teléfono móvil del cliente
    
    # Distribuidora y costos asociados
    distribuidorax = models.CharField(blank=True, max_length=400, null=True)  # Información de la distribuidora
    costAbonado = models.CharField(blank=True, max_length=12, null=True)  # Costo abonado por el cliente
    costTotal = models.CharField(blank=True, max_length=12, null=True)  # Costo total del servicio

    # Descripción del problema reportado
    problem_description = models.TextField(null=False)  # Campo obligatorio para describir el problema
    
    # Fecha de creación de la solicitud (se actualiza automáticamente)
    date = models.DateField(auto_now=True)
    
    # Estado actual de la solicitud
    stat = (
        ('Consulta', 'Consulta'),
        ('Pendiente de investigar', 'Pendiente de investigar'),
        ('Pendiente de enviar', 'Pendiente de enviar'),
        ('Enviado', 'Enviado'),
    )
    status = models.CharField(
        max_length=50, choices=stat, default='Pendiente de enviar', null=True
    )

    # Estado financiero de la solicitud
    estad = (
        ('Consulta', 'Consulta'),
        ('Abonado', 'Abonado'),
        ('Cotizado', 'Cotizado'),
        ('Pagado', 'Pagado'),
    )
    estado = models.CharField(
        max_length=50, choices=estad, default='Consultado', null=True
    )

    # Estado relacionado con el manejo del dinero
    dinomo = (
        ('Vacio', 'Vacio'),
        ('Solicitado pero pendiente de enviarmelo', 'Solicitado pero pendiente de enviarmelo'),
        ('Completado', 'Completado'),
        ('Investigar', 'Investigar'),
    )
    dinomoDis = models.CharField(
        max_length=50, choices=dinomo, default='Vacio', null=True
    )

    # Representación de cadena del objeto
    def __str__(self):
        return self.problem_description

    # Propiedad que concatena el costo abonado y el costo total
    @property
    def dineroCompleto(self):
        components = [self.costAbonado, self.costTotal]
        valid_components = [comp for comp in components if comp is not None]  # Filtrar valores no nulos
        return ' de '.join(valid_components)  # Combinar los valores con "de"

    # Propiedad que combina información básica del vehículo
    @property
    def dineroCompletoss(self):
        components = [self.vehicle_name, self.vehicle_model, self.vehicle_brand]
        valid_components = [comp for comp in components if comp is not None]  # Filtrar valores no nulos
        return ' - '.join(valid_components)  # Combinar los valores con " - "

    # Sobrescribir el método save para realizar modificaciones antes de guardar
    def save(self, *args, **kwargs):
        # Verifica si el campo vehicle_mobile no está vacío
        if self.vehicle_mobile is not None:
            # Elimina espacios en blanco y guiones antes de guardar
            self.vehicle_mobile = self.vehicle_mobile.replace(" ", "").replace("-", "")

        # Limpieza adicional para otros campos (opcional)
        if self.vehicle_brand is not None:
            self.vehicle_brand = self.vehicle_brand.replace("-", "")

        # Llama al método save original para guardar el objeto
        super().save(*args, **kwargs)
