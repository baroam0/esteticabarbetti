from django import forms
from .models import Turno

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['fecha_hora', 'modo_pago', 'pagado', 'comprobante', 'cosmetologa', 'tratamientos', 'observaciones']
        # Los widgets están bien definidos.
        widgets = {
            'fecha_hora': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'modo_pago': forms.Select(attrs={'class': 'form-control'}),
            'comprobante': forms.ClearableFileInput(attrs={'class': 'form-control'}),            
            'cosmetologa': forms.Select(attrs={'class': 'form-control'}),
            'tratamientos': forms.CheckboxSelectMultiple(attrs={'class': 'list-group'}),
        } 