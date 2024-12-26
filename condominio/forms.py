from django import forms
from .models import PerfilUsuario, RegistroVisita, RegistroAutomovil, RegistroMascota, RegistroReporte


class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['integrantes_permanente', 'placas_permanentes']

class RegistroVisitaForm(forms.ModelForm):
    class Meta:
        model = RegistroVisita
        fields = ['personas_visitantes', 'placas_autorizadas']

class RegistroAutomovilForm(forms.ModelForm):
    class Meta:
        model = RegistroAutomovil
        fields = ['auto', 'imagen', 'caracteristicas', 'placa']

class RegistroMascotaForm(forms.ModelForm):
    class Meta:
        model = RegistroMascota
        fields = ['nombre', 'foto', 'caracteristicas']

class RegistroReporteForm(forms.ModelForm):
    class Meta:
        model = RegistroReporte
        fields = ['reporte']