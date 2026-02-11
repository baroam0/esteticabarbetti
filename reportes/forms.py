

from django import forms
from cosmiatras.models import Cosmetologa
from productos.models import Producto


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
        required=True,
        #empty_label="Todos",
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
        
    )

    turno = forms.ChoiceField(
        required=True, 
        choices=[
            ('manana', 'Turno Mañana'), 
            ('tarde', 'Turno Tarde'),
            ('todo', 'Todo el dia')
        ], 
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



class ReporteProductoForm(forms.Form):
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
        required=False,
        empty_label="Todos",
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )        
    )

    producto = forms.ModelChoiceField(
        queryset=Producto.objects.all(), 
        required=False,
        empty_label="Todos",
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )        
    )

