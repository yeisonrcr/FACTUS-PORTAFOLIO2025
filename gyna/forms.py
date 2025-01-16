from django import forms
from django.contrib.auth.models import User
from . import models

        
        
class RequestForm(forms.ModelForm):
    class Meta:
        model = models.Request
        fields = ['tipo', 'vehicle_no', 'vehicle_mobile', 'vehicle_cliente', 'vehicle_name', 
                  'vehicle_model', 'vehicle_brand', 'problem_description', 'distribuidorax', 
                  'costAbonado','costotal',]
        
        

        widgets = {
            'tipo': forms.TextInput(attrs={'class': 'form-control w-full px-4 py-2.5 bg-gray-50 border border-black text-gray-900 rounded-lg focus:ring-2 focus:ring-sky-400 focus:border-sky-400 hover:border-yellow-400 transition-all duration-200'}),
            'vehicle_no': forms.TextInput(attrs={'class': 'form-control w-full px-4 py-2.5 bg-gray-50 border border-black text-gray-900 rounded-lg focus:ring-2 focus:ring-sky-400 focus:border-sky-400 hover:border-yellow-400 transition-all duration-200'}),
            'vehicle_mobile': forms.TextInput(attrs={'class': 'form-control w-full px-4 py-2.5 bg-gray-50 border border-black text-gray-900 rounded-lg focus:ring-2 focus:ring-sky-400 focus:border-sky-400 hover:border-yellow-400 transition-all duration-200'}),
            'vehicle_cliente': forms.TextInput(attrs={'class': 'form-control w-full px-4 py-2.5 bg-gray-50 border border-black text-gray-900 rounded-lg focus:ring-2 focus:ring-sky-400 focus:border-sky-400 hover:border-yellow-400 transition-all duration-200'}),
            'vehicle_name': forms.TextInput(attrs={'class': 'form-control w-full px-4 py-2.5 bg-gray-50 border border-black text-gray-900 rounded-lg focus:ring-2 focus:ring-sky-400 focus:border-sky-400 hover:border-yellow-400 transition-all duration-200'}),
            'vehicle_model': forms.TextInput(attrs={'class': 'form-control w-full px-4 py-2.5 bg-gray-50 border border-black text-gray-900 rounded-lg focus:ring-2 focus:ring-sky-400 focus:border-sky-400 hover:border-yellow-400 transition-all duration-200'}),
            'vehicle_brand': forms.TextInput(attrs={'class': 'form-control w-full px-4 py-2.5 bg-gray-50 border border-black text-gray-900 rounded-lg focus:ring-2 focus:ring-sky-400 focus:border-sky-400 hover:border-yellow-400 transition-all duration-200'}),
            'problem_description': forms.Textarea(attrs={'rows': 3, 'cols': 30, 'class': 'form-control w-full px-4 py-2.5 bg-gray-50 border border-black text-gray-900 rounded-lg focus:ring-2 focus:ring-sky-400 focus:border-sky-400 hover:border-yellow-400 transition-all duration-200'}),
            'distribuidorax': forms.TextInput(attrs={'class': 'form-control w-full px-4 py-2.5 bg-gray-50 border border-black text-gray-900 rounded-lg focus:ring-2 focus:ring-sky-400 focus:border-sky-400 hover:border-yellow-400 transition-all duration-200'}),
            'costAbonado': forms.TextInput(attrs={'class': 'form-control w-full px-4 py-2.5 bg-gray-50 border border-black text-gray-900 rounded-lg focus:ring-2 focus:ring-sky-400 focus:border-sky-400 hover:border-yellow-400 transition-all duration-200'}),
            'costotal': forms.TextInput(attrs={'class': 'form-control w-full px-4 py-2.5 bg-gray-50 border border-black text-gray-900 rounded-lg focus:ring-2 focus:ring-sky-400 focus:border-sky-400 hover:border-yellow-400 transition-all duration-200'}),
            
        }





        
class DistribuidoraxForm(forms.ModelForm):
    class Meta:
        model = models.Request
        fields = ['distribuidorax']  # Agrega otros campos si es necesario



class AdminApproveRequestForm(forms.ModelForm):
    class Meta:
        model = models.Request
        fields = ['status', 'dinomoDis']
    
    stat = (
        ('Consulta', 'Consulta'), 
        ('Pendiente en llegar', 'Pendiente en llegar'), 
        ('Pendiente de investigar', 'Pendiente de investigar'), 
        ('Pendiente de enviar', 'Pendiente de enviar'), 
        ('Compra no entregada', 'Compra no entregada'), 
        ('Compra entregada', 'Compra entregada')
    )
    
    status = forms.ChoiceField(choices=stat)
    
    dinomo = (
        ('Sin estado', 'Sin estado'), 
        ('Monto pagado', 'Monto pagado'), 
        ('Monto pendiente', 'Monto pendiente')
    ) 
    
    dinomoDis = forms.ChoiceField(choices=dinomo)

    
