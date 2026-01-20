

from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required(login_url='/login')
def home(request):
    anio_actual = datetime.now().year    
    return render(
        request, 
        'base.html', 
        {
            'anio_actual': anio_actual
        }
    )


def loginusuario(request):
    if request.POST:
        acceso = authenticate(
            username=request.POST['input-usuario'],
            password=request.POST['input-clave']
        )

        if acceso is not None:
            login(request, acceso)
            return redirect('/')
        else:
            mensaje = "Usuario o Clave invalida."
            return render(
                request,
                'login.html',
                {
                    'mensaje': mensaje,
                })
    else:
        return render(request, 'login.html')


def salir(request):
    logout(request)
    return redirect('/login')

