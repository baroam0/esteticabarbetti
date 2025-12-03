

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


class ImagenMultipleForm(forms.Form):
    imagenes = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}),
        required=False
    )