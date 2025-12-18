from django import forms
from django.forms import inlineformset_factory
from .models import Turno, TurnoProducto


class TurnoProductoForm(forms.ModelForm):
    stock_actual = forms.DecimalField(
        required=False, 
        disabled=True, 
        max_digits=10, 
        decimal_places=2,
        label="Stock Actual"
    )

    class Meta:
        model = TurnoProducto
        fields = ['producto', 'cantidad_consumida']
        widgets = {
            'producto': forms.HiddenInput(), 
            'cantidad_consumida': forms.NumberInput(
                attrs={
                    'class': 'form-control form-control-sm cantidad-consumida', 
                    'step': '0.01', 
                    'min': '0'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            producto = self.instance.producto
            self.fields['stock_actual'].initial = producto.stock


TurnoProductoFormSet = inlineformset_factory(
    Turno, 
    TurnoProducto, 
    form=TurnoProductoForm, 
    extra=0, # No mostrar forms vacíos por defecto
    can_delete=True
)

class TurnoForm(forms.ModelForm):
    class Meta:

        model = Turno

        fields = [
            'fecha_hora', 'monto', 'modo_pago', 'pagado', 'productos',
            'comprobante', 'cosmetologa', 'tratamientos', 'observaciones'
        ]        

        widgets = {
            'fecha_hora': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                },
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


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_hora'].input_formats = ['%Y-%m-%dT%H:%M']

