

from django import forms
from django.forms import inlineformset_factory
from .models import HistoriaClinica, ImagenHistoriaClinica


class HistoriaClinicaForm(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        fields = ['historia', 'diagnostico', 'tratamiento', 'primeravez']
        widgets = {
            'historia': forms.Textarea(attrs={'class': 'form-control', 'rows' : 2}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows' : 2}),
            'tratamiento': forms.Textarea(attrs={'class': 'form-control', 'rows' : 2}),
            'primeravez': forms.CheckboxInput(attrs={'class': 'form-check-input', 'rows' : 2}),
        }


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        default_attrs = {"multiple": True}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


class ImagenMultipleForm(forms.Form):
    imagenes = forms.FileField(
        widget=MultipleFileInput(attrs={
            "name": "imagenes[]",
        }),
        required=False
    )

