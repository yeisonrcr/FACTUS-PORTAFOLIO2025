from .models import ModeloAnio, AnioAuto
from django import forms
from .models import Marca, Modelo, Repuesto, Comentario, Carrito, ItemCarrito, Categoria, ImagenRepuesto

class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre']

class ModeloForm(forms.ModelForm):
    class Meta:
        model = Modelo
        fields = ['nombre', 'marca']


class ModeloAnioForm(forms.ModelForm):
    anios = forms.ModelMultipleChoiceField(
        queryset=AnioAuto.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    
    class Meta:
        model = ModeloAnio
        fields = ['modelo', 'anios']  # Asegúrate de incluir 'anios' aquí
    
    def save(self, commit=True):
        modelo_anio = super().save(commit=False)
        if commit:
            modelo_anio.save()
            modelo_anio.anios.set(self.cleaned_data['anios'])
        return modelo_anio






class ImagenRepuestoForm(forms.ModelForm):
    class Meta:
        model = ImagenRepuesto
        fields = ['imagen', 'es_principal', 'orden']

class RepuestoForm(forms.ModelForm):
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    modelos_anios_compatibles = forms.ModelMultipleChoiceField(
        queryset=ModeloAnio.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Repuesto
        fields = ['nombre', 'codigo', 'descripcion', 'precio', 'stock', 'modelos_anios_compatibles', 'categorias', 'en_oferta', 'oferta_especial']
        
    def save(self, commit=True):
        repuesto = super().save(commit=False)
        if commit:
            repuesto.save()
            self.save_m2m()  # Guardar relaciones ManyToMany
        return repuesto




























class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['repuesto', 'texto', 'calificacion']

class CarritoForm(forms.ModelForm):
    class Meta:
        model = Carrito
        fields = ['usuario', 'activo']

class ItemCarritoForm(forms.ModelForm):
    class Meta:
        model = ItemCarrito
        fields = ['carrito', 'repuesto', 'cantidad']

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre','descripcion']
