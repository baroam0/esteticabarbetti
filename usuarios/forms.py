

from django import forms
from django.contrib.auth.models import User


class UsuarioForm(forms.ModelForm):
    username = forms.CharField(
        label="Nombre de login", 
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de login'})
    )

    first_name = forms.CharField(
        label="Nombre", 
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Nombre'})
    )

    last_name = forms.CharField(
        label="Apellido", 
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Apellido'})
    )
    
    password = forms.CharField(
        label="Password", 
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control form-control-user'
            })

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password"]

