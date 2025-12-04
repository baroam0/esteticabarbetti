
from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Cosmiatra, Cosmetologa
from .forms import CosmiatraForm, CosmetologaForm


@login_required
def listar_cosmiatra(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        cosmiatras = Cosmiatra.objects.filter(username__contains=parametro)
    else:
        cosmiatras = Cosmiatra.objects.all().order_by("last_name")
    paginador = Paginator(cosmiatras, 15)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    usuarios = paginador.get_page(page)
    return render(request, 'cosmiatras/lista_cosmiatra.html', {'usuarios': usuarios})

@login_required
def crear_cosmiatra(request):
    if request.method == 'POST':
        form = CosmiatraForm(request.POST)
        if form.is_valid():
            cosmiatra = form.save(commit=False)
            cosmiatra.set_password(form.cleaned_data['password'])  # importante para User
            cosmiatra.save()
            return redirect('cosmiatra_list')
    else:
        form = CosmiatraForm()
    return render(request, 'cosmiatras/crear_cosmiatra.html', {'form': form})


@login_required
def editar_cosmiatra(request, pk):
    cosmiatra = get_object_or_404(Cosmiatra, pk=pk)
    if request.method == 'POST':
        form = CosmiatraForm(request.POST, instance=cosmiatra)
        if form.is_valid():
            cosmiatra = form.save(commit=False)
            if form.cleaned_data['password']:
                cosmiatra.set_password(form.cleaned_data['password'])
            cosmiatra.save()
            return redirect('listar_cosmiatra')
    else:
        form = CosmiatraForm(instance=cosmiatra)
    return render(request, 'cosmiatras/crear_cosmiatra.html', {'form': form})


@login_required
def listar_cosmetologa(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        cosmetologas = Cosmetologa.objects.filter(username__contains=parametro)
    else:
        comsetologas = Cosmetologa.objects.all().order_by("apellido")
    paginador = Paginator(comsetologas, 15)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(request, 'cosmiatras/lista_cosmetologa.html', {'resultados': resultados})


@login_required
def crear_cosmetologa(request):
    if request.method == 'POST':
        form = CosmetologaForm(request.POST)
        if form.is_valid():
            cosmetologa = form.save(commit=False)
            cosmetologa.save()
            return redirect('listar_cosmetologa')
    else:
        form = CosmetologaForm()
    return render(
        request, 
        'cosmiatras/crear_cosmetologa.html', 
        {
            'accion': 'Crear',
            'form': form
        }
    )


@login_required
def editar_cosmetologa(request, pk):
    cosmetologa = get_object_or_404(Cosmetologa, pk=pk)
    if request.method == 'POST':
        form = CosmetologaForm(request.POST, instance=cosmetologa)
        if form.is_valid():
            cosmetologaform = form.save(commit=False)
            cosmetologaform.save()
            return redirect('listar_cosmetologa')
    else:
        form = CosmetologaForm(instance=cosmetologa)
    return render(
        request, 
        'cosmiatras/crear_cosmetologa.html', 
        {
            'accion': 'Editar',
            'form': form
        }
    )


# Create your views here.
