
import json

from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404


from .forms import PacienteForm
from .models import Paciente
from historiasclinicas.models import HistoriaClinica
from turnos.models import Turno


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
        "dni": p.numerodocumento or ""
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


@login_required
def buscar_pacientes_tratamiento(request):

    MESES = { 
        1: "Enero", 
        2: "Febrero", 
        3: "Marzo", 
        4: "Abril", 
        5: "Mayo", 
        6: "Junio", 
        7: "Julio", 
        8: "Agosto", 
        9: "Septiembre", 
        10: "Octubre", 
        11: "Noviembre", 
        12: "Diciembre",
    }

    parametro = request.GET.get('q', '')
    page_number = request.GET.get('page', 1)

    if parametro:
        if parametro.isdigit():
            turnos =  Turno.objects.filter(
                numerodocumento__icontains=parametro
            ).order_by("-fecha_hora")
        else:
            turnos =  Turno.objects.filter(
                nombrepaciente__icontains=parametro
            ).order_by("-nombrepaciente")
        paginator = Paginator(turnos, 10)
        page_obj = paginator.get_page(page_number)

        data = [{
            "id": p.pk,
            "nombre": p.nombrepaciente,
            "fecha_hora": f"{p.fecha_hora.day} {MESES[p.fecha_hora.month]} {p.fecha_hora.year} {p.fecha_hora.strftime('%H:%M')}", 
            "dni": p.numerodocumento or "",
            "tratamientos": " - ".join([t.descripcion for t in p.tratamientos.all()]), 
            "sexo": p.sexo
        } for p in page_obj]


        return JsonResponse({
            "results_turnopaciente": data,
            "page_turnopaciente": page_obj.number,
            "total_pages_turnopaciente": paginator.num_pages,
            "has_next_turnopaciente": page_obj.has_next(),
            "has_previous_turnopaciente": page_obj.has_previous(),
            "next_page_turnopaciente": page_obj.next_page_number() if page_obj.has_next() else None,
            "prev_page_turnopaciente": page_obj.previous_page_number() if page_obj.has_previous() else None,
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


def eliminar_paciente(request, pk):
    paciente = Paciente.objects.get(pk=pk)
    historiaclinica = HistoriaClinica.objects.filter(paciente=paciente)

    if request.method == "POST":
        historiaclinica.delete()
        paciente.delete()
        return redirect(
            reverse(
                "listar_pacientes"
            )
        )

    return render(
        request, 
        "pacientes/eliminar_paciente.html", 
        {
            "historiaclinica": historiaclinica,
            "paciente": paciente
        }
    )


def unificar_paciente(request):
    return render(request, 'pacientes/unificar_paciente.html')


def unificar_buscar_pacientes(request):
    parametro = request.GET.get('q', '')
    page_number = request.GET.get('page', 1)

    if parametro:
        if parametro.isdigit():
            pacientes = Paciente.objects.filter(
                numerodocumento__icontains=parametro
            ).order_by("nombre")
        else:
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
        "sexo": p.sexo,
        "dni": p.numerodocumento or "",
        "fechanacimiento": p.fechanacimiento or ""
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


def unificar_proceso_paciente(request):
    if request.method == "POST":
        data = json.loads(request.body)
        base_id = data.get("base_id")
        asimilar_id = data.get("asimilar_id")
        pacientebase = Paciente.objects.get(pk=base_id)
        pacienteasimilar = Paciente.objects.get(pk=asimilar_id)
        historiasclinicas = HistoriaClinica.objects.filter(paciente=pacienteasimilar)

        for hc in historiasclinicas:
            hc.paciente=pacientebase
            hc.save()
        pacienteasimilar.delete()
        return JsonResponse({"message": f"Pacientes unificados"})
    return JsonResponse({"error": "Método no permitido"}, status=405)


def crear_paciente_precarga(request, pk):
    if request.method == 'POST':
        form = PacienteForm(request.POST, request.FILES)
        if form.is_valid():
            paciente=form.save()
            nuevo_id=paciente.id
            return redirect('listar_historiasclinicas', pk=nuevo_id)
    else:
        turno=Turno.objects.get(pk=pk)
        form = PacienteForm(
            initial={
                "nombre": turno.nombrepaciente,
                "numerodocumento": turno.numerodocumento,
                'sexo': turno.sexo
            }
        )

    return render(
        request, 
        'pacientes/crear_paciente.html', 
        {
            'form': form, 
            'accion': 'Nuevo '
        }
    )

# Create your views here.
