


from django import forms
from cosmiatras.models import Cosmetologa


class ReporteCosmiatraForm(forms.Form):
    fecha_desde = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        )
    )
    
    fecha_hasta = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        )
    )

    cosmiatra = forms.ModelChoiceField(
        queryset=Cosmetologa.objects.all(), 
        #empty_label="Todos",
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
        
    )
    
    porcentaje = forms.DecimalField(
        required=True,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={'class': 'form-control'}
        )
    )
