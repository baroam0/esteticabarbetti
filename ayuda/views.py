
from django.shortcuts import render


def inicio(request):
    # Puedes pasar contexto al template si lo necesitas
    contexto = {
        "titulo": "Bienvenido",
        "mensaje": "Esta es una vista basada en función en Django 5.1.3",
    }
    return render(request, "ayuda/main.html", contexto)


def tratamientos(request):
    return render(request, "ayuda/tratamientos.html")



# Create your views here.
