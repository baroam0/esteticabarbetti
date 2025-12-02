
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PacienteForm
from .models import Paciente


@login_required
def listar_pacientes(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        pacientes = Paciente.objects.filter(nombre__contains=parametro)
    else:
        pacientes = Paciente.objects.all().order_by("nombre")
    paginador = Paginator(pacientes, 10)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1

    pacientes = paginador.get_page(page)
    return render(request, 'pacientes/lista_pacientes.html', {'pacientes': pacientes})


from django.http import JsonResponse

@login_required
def buscar_pacientes(request):
    parametro = request.GET.get('q', '')
    pacientes = Paciente.objects.filter(nombre__icontains=parametro).order_by("nombre")[:10]

    data = []
    for p in pacientes:
        data.append({
            "id": p.pk,
            "nombre": p.nombre,
            "edad": p.edad(),
            "domicilio": p.domicilio,
        })
    return JsonResponse(data, safe=False)


def crear_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect('listar_pacientes') 

    else:
        form = PacienteForm()

    return render(request, 'pacientes/crear_paciente.html', {
        'form': form, 'accion': 'Nuevo '})


def editar_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)

    if request.method == 'POST':
        form = PacienteForm(request.POST, request.FILES, instance=paciente)    

        if form.is_valid():
            
            form.save() 
            return redirect('listar_pacientes') 
    
    else:
        form = PacienteForm(instance=paciente)

    context = {
        'form': form,
        'accion': 'Editar'
    }
    return render(request, 'pacientes/crear_paciente.html', context)

# Create your views here.
