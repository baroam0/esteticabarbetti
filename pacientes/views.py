
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404


from .forms import PacienteForm
from .models import Paciente


@login_required
def listar_pacientes(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        pacientes =  Paciente.objects.filter(nombre__contains=parametro)
    else:
        pacientes =  Paciente.objects.all().order_by("nombre")
    paginador = Paginator(pacientes, 10)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)

    return render(request, 'pacientes/lista_pacientes.html', {'results': resultados})


@login_required
def buscar_pacientes(request):
    parametro = request.GET.get('q', '')
    page_number = request.GET.get('page', 1)

    if parametro:
        pacientes = Paciente.objects.filter(
            nombre__icontains=parametro
        ).order_by("nombre")
    else:
        pacientes = Paciente.objects.all().order_by("nombre")

    paginator = Paginator(pacientes, 10)
    page_obj = paginator.get_page(page_number)

    data = [{
        "id": p.pk,
        "nombre": p.nombre,
        "edad": p.edad(),
        "domicilio": p.domicilio
    } for p in page_obj]

    return JsonResponse({
        "results": data,
        "page": page_obj.number,
        "total_pages": paginator.num_pages,
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous(),
        "next_page": page_obj.next_page_number() if page_obj.has_next() else None,
        "prev_page": page_obj.previous_page_number() if page_obj.has_previous() else None,
    })


def crear_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST, request.FILES)
        if form.is_valid():
            paciente=form.save()
            nuevo_id=paciente.id
            return redirect('listar_historiasclinicas', pk=nuevo_id)
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
            messages.success(request, "Paciente actualizado correctamente.") 
            return redirect('/pacientes/editar/' + str(pk))
        else:
            messages.error(request, "Hay errores en el formulario.") 
    
    else:
        form = PacienteForm(instance=paciente)

    context = {
        'form': form,
        'accion': 'Editar',
        'pk': pk
    }
    return render(request, 'pacientes/crear_paciente.html', context)

# Create your views here.
