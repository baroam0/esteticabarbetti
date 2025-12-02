

from django import forms
from .models import HistoriaClinica, ImagenHistoriaClinica

class HistoriaClinicaForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(HistoriaClinicaForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            if field == "is_active":
                self.fields[field].widget.attrs.update({
                    'class': 'custom-control-input'
                })
            else:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control form-control-user'
                })

    class Meta:
        model = HistoriaClinica
        fields = [
            'historia',
            'diagnostico',
            'tratamiento',
            
        ]

        widgets = {
            'historia': forms.Textarea(attrs={'rows': 1}),
            'diagnostico': forms.Textarea(attrs={'rows': 1}),
            'tratamiento': forms.Textarea(attrs={'rows': 1}),
        }


class ImagenHistoriaClinicaForm(forms.ModelForm):
    imagen = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = ImagenHistoriaClinica
        fields = ['imagen']