from django import forms
from django.core.exceptions import ValidationError #utilizaremos validadores 
from .models import Tienda, Producto, Categoria, Provincia, Canton, Distrito

class ProvinciaForm(forms.ModelForm):
    """
    Formulario para creación y edición de Provincias
    Hereda de ModelForm para validación automática
    """
    class Meta:
        model = Provincia
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'})
        }

class CantonForm(forms.ModelForm):
    """
    Formulario para creación y edición de Cantones
    Incluye validación de provincia
    """
    class Meta:
        model = Canton
        fields = ['nombre', 'provincia']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'provincia': forms.Select(attrs={'class': 'form-control'})
        }

class DistritoForm(forms.ModelForm):
    """
    Formulario para creación y edición de Distritos
    Validación de cantón incluida
    """
    class Meta:
        model = Distrito
        fields = ['nombre', 'canton']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'canton': forms.Select(attrs={'class': 'form-control'})
        }

class CategoriaForm(forms.ModelForm):
    """
    Formulario para creación y edición de Categorías
    Incluye validación de nombre único
    """
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def clean_nombre(self):
        """
        Validación personalizada para garantizar nombres únicos
        """
        nombre = self.cleaned_data['nombre']
        if Categoria.objects.filter(nombre__iexact=nombre).exists(): #si existe alguno
            raise ValidationError(f"Ya existe una categoría con este nombre: -> {nombre}") #se envia un error
        return nombre

class TiendaForm(forms.ModelForm):
    """
    Formulario para creación y edición de Tiendas
    Incluye validaciones y widgets personalizados
    """
    class Meta:
        model = Tienda
        fields = [
            'nombre', 'eslogan', 'logo', 
            'provincia', 'canton', 'distrito', 'pueblo'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500'
            }),
            'eslogan': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500'
            }),
            'logo': forms.FileInput(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:bg-green-100 file:text-green-700 hover:file:bg-green-200'
            }),
            'provincia': forms.Select(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500'
            }),
            'canton': forms.Select(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500'
            }),
            'distrito': forms.Select(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500'
            }),
            'pueblo': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500'
            }),
        }


    def clean_logo(self):
        """
        Validación de tamaño y tipo de imagen para logo
        """
        logo = self.cleaned_data.get('logo') #obtengo y guardo el logo en una variable
        try:
            if logo: #si hay logo
            # Limitar tamaño de imagen (5MB)
        
                if logo.size > 5 * 1024 * 1024: #es muy grande el logo
                    raise ValidationError("El tamaño del logo no debe exceder 5MB.")
                
                # Validar tipo de archivo
                valid_types = ['image/jpeg', 'image/png', 'image/gif']
                if logo.content_type not in valid_types:
                    raise ValidationError("Formato de imagen no válido. Use JPEG, PNG o GIF.")
                
        except Exception as e:
                raise e
                
        return logo

class ProductoForm(forms.ModelForm):
    """
    Formulario para creación y edición de Productos
    Validaciones exhaustivas para datos del producto
    """
    class Meta:
        model = Producto
        fields = [
            'nombre', 'categoria', 
            'precio', 'stock', 
            'foto1', 'foto2', 'foto3','detalles', 
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500'
            }),
            'categoria': forms.Select(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500',
                'step': '0.01'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500'
            }),
            'foto1': forms.FileInput(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:bg-green-100 file:text-green-700 hover:file:bg-green-200'
            }),
            'foto2': forms.FileInput(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:bg-green-100 file:text-green-700 hover:file:bg-green-200'
            }),
            'foto3': forms.FileInput(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:bg-green-100 file:text-green-700 hover:file:bg-green-200'
            }),
            'detalles': forms.Textarea(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500',
                'rows': 4
            }),
        }


    def clean_precio(self):
        """
        Validación de precio positivo
        """
        precio = self.cleaned_data['precio']
        try:
            if precio <= 0:
                raise ValidationError("El precio debe ser mayor a cero.")
        except Exception as e:
            raise e
            
        return precio

    def clean_stock(self):
        """
        Validación de stock positivo
        """
        stock = self.cleaned_data['stock']
        try:
            if stock < 0:
                raise ValidationError("El stock no puede ser negativo.")
        except Exception as e:
            raise e
        return stock

    def clean(self):
        """
        Validación de múltiples campos
        Limita a máximo 3 imágenes
        """
        #obtengo las imagenes del padre
        cleaned_data = super().clean()
        fotos = [cleaned_data.get('foto1'), 
                 cleaned_data.get('foto2'), 
                 cleaned_data.get('foto3')]
        
        # Validar tamaño de imágenes
        try:
            for foto in fotos:
                if foto:
                    if foto.size > 5 * 1024 * 1024:  # 5MB
                        raise ValidationError("Cada imagen no debe exceder 5MB.")
                    
                    valid_types = ['image/jpeg', 'image/png', 'image/gif']
                    if foto.content_type not in valid_types:
                        raise ValidationError("Solo se permiten imágenes JPEG, PNG o GIF.")
        except Exception as e:
            raise e

        return cleaned_data

class CarritoForm(forms.Form):
    """
    Formulario personalizado para manejo de Carrito
    Permite agregar/modificar productos
    """
    try:
        producto_id = forms.IntegerField(widget=forms.HiddenInput()) #id del producto seleccionado
        cantidad = forms.IntegerField( #seleccionamos cantidad por defecto 1
            min_value=1, 
            initial=1,
            widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}) #front del select
        )
    except Exception as e:
        raise e
        

    def clean_cantidad(self):
        """
        Validación de cantidad , si hay mas o menos de lo seleccionado por el usuario
        """
        cantidad = self.cleaned_data['cantidad']
        try:
            producto_id = self.cleaned_data.get('producto_id')
            
            if producto_id:
                producto = Producto.objects.get(id=producto_id)
                if cantidad > producto.stock:
                    raise ValidationError(f"Solo hay {producto.stock} unidades disponibles.")
        except Exception as e:
            raise e
            
        
        return cantidad