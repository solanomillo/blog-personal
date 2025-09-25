from django import forms
from .models import Comentario, Publicacion


class ComentarioForm(forms.ModelForm):
    """
    Formulario para comentarios.
    """
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Escribe tu comentario aquí...'
            }),
        }
        labels = {
            'contenido': 'Comentario'
        }


class PublicacionForm(forms.ModelForm):
    """
    Formulario para publicaciones.
    """
    class Meta:
        model = Publicacion
        fields = [
            'titulo', 'slug', 'resumen', 'contenido', 
            'categoria', 'imagen_destacada', 'tags', 'estado'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'resumen': forms.Textarea(attrs={
                'rows': 3, 
                'class': 'form-control'
            }),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contenido'].required = True