

from django import forms
from .models import Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'idaccess',
            'nombre',
            'fechanacimiento',
            'sexo',
            'estadocivil',
            'numerodocumento',
            'domicilio',
            'correoelectronico',
            'obrasocial',
            'telefono',
            'notas',
            'proximoturno',
            'foto',
            'aviso',
        ]
        widgets = {
            'fechanacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'estadocivil': forms.TextInput(attrs={'class': 'form-control'}),
            'numerodocumento': forms.TextInput(attrs={'class': 'form-control'}),
            'domicilio': forms.TextInput(attrs={'class': 'form-control'}),
            'correoelectronico': forms.EmailInput(attrs={'class': 'form-control'}),
            'obrasocial': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'proximoturno': forms.TextInput(attrs={'class': 'form-control'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'aviso': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
