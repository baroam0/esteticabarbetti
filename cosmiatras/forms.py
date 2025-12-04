

from django import forms
from .models import Cosmiatra, Cosmetologa

class CosmiatraForm(forms.ModelForm):
    class Meta:
        model = Cosmiatra
        fields = ['username', 'first_name', 'last_name',  'telefono', 'password']  # ajusta según lo que quieras mostrar
        widgets = {
            'password': forms.PasswordInput(),
        }



class CosmetologaForm(forms.ModelForm):
    class Meta:
        model = Cosmetologa
        fields = ['nombre', 'apellido',  'telefono']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefono'})         
        }
        