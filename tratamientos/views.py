
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .forms import TratamientoForm
from .models import Tratamiento


@login_required
def listar_tratamientos(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        tratamientos = Tratamiento.objects.filter(descripcion__contains=parametro)
    else:
        tratamientos = Tratamiento.objects.all().order_by("descripcion")
    paginador = Paginator(tratamientos, 15)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(request, 'tratamientos/lista_tratamientos.html', {'resultados': resultados})


@login_required
def crear_tratamiento(request):
    if request.method == 'POST':
        form = TratamientoForm(request.POST)
        if form.is_valid():
            tratamiento = form.save(commit=False)
            tratamiento.usuario = request.user 
            tratamiento.save()
            return redirect('listar_tratamientos')
    else:
        form = TratamientoForm()
    return render(request, 'tratamientos/crear_tratamiento.html', {'form': form, 'accion': 'Crear'})


@login_required
def editar_tratamiento(request, pk):
    #tratamiento = get_object_or_404(Tratamiento, pk=pk, usuario=request.user)  
    tratamiento = get_object_or_404(Tratamiento, pk=pk)
    if request.method == 'POST':
        form = TratamientoForm(request.POST, instance=tratamiento)
        if form.is_valid():
            form.save()
            return redirect('listar_tratamientos')
    else:
        form = TratamientoForm(instance=tratamiento)
    return render(request, 'tratamientos/crear_tratamiento.html', {'form': form, 'accion': 'Editar'})


# Create your views here.
