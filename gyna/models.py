from django.db import models
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError


def validate_positive_integer(value):
    if not isinstance(value, int) or value < 5:
        raise ValidationError("El valor debe ser un número entero positivo.")


class Request(models.Model):

    tipo = models.CharField(blank=True,max_length=40,null=True,default='Internet')
    
    vehicle_no = models.CharField(blank=True,max_length=17,null=True)
    vehicle_name = models.CharField(blank=True,max_length=50,null=True )
    vehicle_model = models.CharField(blank=True,max_length=40,null=True)
    vehicle_brand = models.CharField(blank=True,max_length=15,null=True)
    vehicle_cliente = models.CharField(blank=True,max_length=80,null=True)
    vehicle_mobile = models.CharField(max_length=15,null=True, blank=True)    
    distribuidorax= models.CharField(blank=True,max_length=400,null=True)
    costAbonado= models.CharField(blank=True,max_length=100,null=True, default='0')
    costotal = models.CharField(blank=True,max_length=100,null=True, default='0')
    
    problem_description = models.TextField(null=False)
    date=models.DateField(auto_now=True)
    
    
    
    
    
    stat = ( ('Consulta', 'Consulta'), ('Pendiente en llegar', 'Pendiente en llegar'), ('Pendiente de investigar', 'Pendiente de investigar'), ('Pendiente de enviar', 'Pendiente de enviar'), ('Compra no entregada', 'Compra no entregada'), ('Compra entregada', 'Compra entregada') )
    
    
    dinomo = ( ('Sin estado', 'Sin estado'),('Pendiente', 'Pendiente'), ('Completado', 'Completado'), ('Monto pagado', 'Monto pagado'), ('Monto pendiente', 'Monto pendiente'), ) 
    status = models.CharField(max_length=50, choices=stat, default='Consulta', null=True) 
    
    
    
    
    dinomoDis = models.CharField(max_length=50, choices=dinomo, default='Sin estado', null=True)
    
    
    
    def __str__(self):
        return self.problem_description
        
    @property
    def dineroCompleto(self):
        components = [self.costAbonado]
        valid_components = [comp for comp in components if comp is not None]
        return ' de '.join(valid_components)

    
    @property
    def dineroCompletoss(self):
        components = [self.vehicle_name, self.vehicle_model, self.vehicle_brand]
        valid_components = [comp for comp in components if comp is not None]
        return ' - '.join(valid_components)


    def save(self, *args, **kwargs):
        # Verifica si el campo vehicle_mobile no está vacío
        if self.vehicle_mobile is not None:
            # Elimina espacios en blanco y guiones antes de guardar
            self.vehicle_mobile = self.vehicle_mobile.replace(" ", "")
            self.vehicle_mobile = self.vehicle_mobile.replace("-", "")
        
        # Repite lo mismo para otros campos si es necesario
        if self.vehicle_brand is not None:
            self.vehicle_brand = self.vehicle_brand.replace("-", "")
        
        super().save(*args, **kwargs)
        
        
        