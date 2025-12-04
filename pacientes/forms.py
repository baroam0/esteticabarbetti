

from django import forms
from .models import Paciente

class PacienteForm(forms.ModelForm):
    fechanacimiento = forms.DateField(
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={'type': 'date', 'class': 'form-control'}
        ),
        input_formats=['%Y-%m-%d']
    )

    def __init__(self, *args, **kwargs):
            super(PacienteForm, self).__init__(*args, **kwargs)
            
            for field in iter(self.fields):
                    self.fields[field].widget.attrs.update({
                        'class': 'form-control form-control-user'
                    })
            

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

        labels = {
            'foto': 'Elegir imagen',
        }

        widgets = {
            'fechanacimiento': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control', 'required' : 'False'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido y Nombre'}),
            'estadocivil': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estado Civil'}),
            'numerodocumento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numero Documento'}),
            'domicilio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Domicilio'}),
            'correoelectronico': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electronico' }),
            'obrasocial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Obra Social'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefono'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Notas...'}),
            'proximoturno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Proximo turno'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'aviso': forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'placeholder': 'Aviso'}),
        }
