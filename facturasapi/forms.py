from django import forms
from .models import Cliente, Factura, DetalleFactura

class ClienteForm(forms.ModelForm):
    """Form for client information"""
    class Meta:
        model = Cliente
        fields = ['nit', 'razon_social', 'direccion', 'email', 'telefono']
        widgets = {
            'nit': forms.TextInput(attrs={'class': 'form-control'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

class FacturaForm(forms.ModelForm):
    """Form for invoice information"""
    class Meta:
        model = Factura
        fields = ['numero_factura', 'cliente', 'valor_total']
        widgets = {
            'numero_factura': forms.TextInput(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'valor_total': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class DetalleFacturaForm(forms.ModelForm):
    """Form for invoice detail items"""
    class Meta:
        model = DetalleFactura
        fields = ['descripcion', 'cantidad', 'valor_unitario', 'valor_total']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_total': forms.NumberInput(attrs={'class': 'form-control'}),
        }