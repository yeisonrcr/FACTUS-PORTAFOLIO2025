from django import forms  # Importar la biblioteca forms de Django
from .models import Cliente, Facturax, DetalleFactura  # Importar los modelos Cliente, Facturax y DetalleFactura

class ClienteForm(forms.ModelForm):
    """Formulario para la información del cliente"""
    class Meta:
        model = Cliente  # Modelo asociado: Cliente
        fields = ['nit', 'razon_social', 'direccion', 'email', 'telefono']  # Campos del modelo a incluir en el formulario
        widgets = {
            'nit': forms.TextInput(attrs={'class': 'form-control'}),  # Widget de entrada de texto para el NIT
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),  # Widget de entrada de texto para la razón social
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),  # Widget de entrada de texto para la dirección
            'email': forms.EmailInput(attrs={'class': 'form-control'}),  # Widget de entrada de texto para el email
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),  # Widget de entrada de texto para el teléfono
        }

class FacturaForm(forms.ModelForm):
    """Formulario para la información de la factura"""
    class Meta:
        model = Facturax  # Modelo asociado: Facturax
        fields = ['numero_factura', 'cliente', 'valor_total']  # Campos del modelo a incluir en el formulario
        widgets = {
            'numero_factura': forms.TextInput(attrs={'class': 'form-control'}),  # Widget de entrada de texto para el número de factura
            'cliente': forms.TextInput(attrs={'class': 'form-control'}),   # Widget de selección para el cliente
            'valor_total': forms.NumberInput(attrs={'class': 'form-control'}),  # Widget de entrada numérica para el valor total
        }

class DetalleFacturaForm(forms.ModelForm):
    """Formulario para los ítems del detalle de la factura"""
    class Meta:
        model = DetalleFactura  # Modelo asociado: DetalleFactura
        fields = ['descripcion', 'cantidad', 'valor_unitario', 'valor_total']  # Campos del modelo a incluir en el formulario
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),  # Widget de entrada de texto para la descripción
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),  # Widget de entrada numérica para la cantidad
            'valor_unitario': forms.NumberInput(attrs={'class': 'form-control'}),  # Widget de entrada numérica para el valor unitario
            'valor_total': forms.NumberInput(attrs={'class': 'form-control'}),  # Widget de entrada numérica para el valor total
        }
