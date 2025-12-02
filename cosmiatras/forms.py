

from django import forms
from .models import Cosmiatra

class CosmiatraForm(forms.ModelForm):
    class Meta:
        model = Cosmiatra
        fields = ['username', 'first_name', 'last_name',  'telefono', 'password']  # ajusta según lo que quieras mostrar
        widgets = {
            'password': forms.PasswordInput(),
        }
