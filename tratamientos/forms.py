

from django import forms
from .models import Tratamiento


class TratamientoForm(forms.ModelForm):
    descripcion = forms.CharField(
        label="Descripcion", 
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Descripcion'})
    )

    precio = forms.DecimalField(
        label="Precio"
    )
    
    def __init__(self, *args, **kwargs):
        super(TratamientoForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control form-control-user'
            })

    class Meta:
        model = Tratamiento
        fields = ["descripcion", "precio"]

