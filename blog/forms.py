from django import forms
from .models import Blog


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['titulo_blog', 'slug_blog', 'resumen_blog', 'caracteristica_blog', 'explicacion_blog', 'youtube_blog', 'codigo_blog', 'imagen_blog']

        # Personalizamos widgets para los campos visibles:
        widgets = {
            'titulo_blog': forms.TextInput(attrs={'class': 'form-control'}),
            'slug_blog': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Slug para la URL (opcional)'}),
            'resumen_blog': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'caracteristica_blog': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'explicacion_blog': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'youtube_blog': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_blog': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'imagen_blog': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si se quisiera hacer algo adicional en la inicialización, se puede agregar aquí.
        # Si el objeto ya tiene un slug, no lo editamos manualmente
        self.fields['slug_blog'].required = False

    def clean_imagen_blog(self):
        """
        Realiza la validación personalizada para la imagen del blog.
        Aquí puedes agregar restricciones como tamaño máximo o tipo de imagen.
        """
        imagen = self.cleaned_data.get('imagen_blog')
        # Ejemplo de validación para el tamaño de la imagen (opcional).
        if imagen and imagen.size > 5 * 1024 * 1024:  # Limitar a 5MB
            raise forms.ValidationError("La imagen no debe superar los 5MB.")
        return imagen
