from django import forms
from django.contrib.auth.models import User
from . import models

# Formulario principal para manejar solicitudes relacionadas con vehículos
class RequestForm(forms.ModelForm):
    class Meta:
        model = models.Request  # Modelo asociado a este formulario
        fields = [
            'tipo', 'vehicle_no', 'vehicle_mobile', 'vehicle_cliente', 
            'vehicle_name', 'vehicle_model', 'vehicle_brand', 
            'problem_description', 'distribuidorax', 'costAbonado', 'costTotal'
        ]  # Campos que serán incluidos en el formulario

        # Personalización de widgets para algunos campos
        widgets = {
            'problem_description': forms.Textarea(attrs={'rows': 3, 'cols': 30})  # Área de texto con tamaño definido
        }

# Formulario para manejar la información específica de distribuidoras
class DistribuidoraxForm(forms.ModelForm):
    class Meta:
        model = models.Request  # Modelo asociado a este formulario
        fields = ['distribuidorax']  # Campo incluido en el formulario (se pueden agregar más si es necesario)

# Formulario para que el administrador apruebe y actualice solicitudes
class AdminApproveRequestForm(forms.Form):
    # Campo para capturar el costo abonado
    costAbonado = forms.CharField()
    
    # Opciones para el estado general de la solicitud
    stat = (
        ('Consulta', 'Consulta'),
        ('Pendiente de investigar', 'Pendiente de investigar'),
        ('Pendiente de enviar', 'Pendiente de enviar'),
        ('Enviado', 'Enviado')
    )
    status = forms.ChoiceField(choices=stat)  # Campo de selección para el estado general
    
    # Opciones para el estado financiero de la solicitud
    estad = (
        ('Consulta', 'Consulta'),
        ('Abonado', 'Abonado'),
        ('Cotizado', 'Cotizado'),
        ('Pagado', 'Pagado')
    )
    estado = forms.ChoiceField(choices=estad)  # Campo de selección para el estado financiero
    
    # Opciones para el estado relacionado con distribuidoras
    dinomo = (
        ('Vacio', 'Vacio'),
        ('Solicitado pero pendiente de enviarmelo', 'Solicitado pero pendiente de enviarmelo'),
        ('Completado', 'Completado'),
        ('Investigar', 'Investigar')
    )
    dinomoDis = forms.ChoiceField(choices=dinomo)  # Campo de selección para el estado de la distribuidora
