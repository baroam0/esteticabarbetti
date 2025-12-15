from django import forms
from .models import Turno

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno

        fields = [
            'fecha_hora', 'monto', 'modo_pago', 'pagado', 
            'comprobante', 'cosmetologa', 'tratamientos', 'productos', 'observaciones'
        ]

        widgets = {
            'fecha_hora': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class':'form-control'},
                format='%Y-%m-%dT%H:%M'
            ),
            'monto': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.01',
                    'min': '0',
                    'placeholder': 'Ingrese el monto'
                }
            ),
            'modo_pago': forms.Select(attrs={'class': 'form-control'}),
            'comprobante': forms.ClearableFileInput(attrs={'class': 'form-control'}),            
            'cosmetologa': forms.Select(attrs={'class': 'form-control'}),
            'tratamientos': forms.CheckboxSelectMultiple(),
            'productos': forms.CheckboxSelectMultiple(),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2 }),
        }