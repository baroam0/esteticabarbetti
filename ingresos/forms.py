

from django import forms
from .models import Categoria


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['descripcion', 'habilitado'] 
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            #'habilitado': forms.CheckboxInput(attrs={'class': 'custom-control-input', 'id': 'id_habilitado'}),
        }
