

from django.db import IntegrityError
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import TratamientoForm
from .models import Tratamiento


MESES = {
    1: "Ene.",
    2: "Feb.",
    3: "Mar.",
    4: "Abr.",
    5: "May.",
    6: "Jun.",
    7: "Jul.",
    8: "Ago.",
    9: "Sep.",
    10: "Oct.",
    11: "Nov.",
    12: "Dic.",
}


def formatear_fecha(fecha):
    fecha_local = timezone.localtime(fecha)
    dia = fecha_local.day
    mes = MESES[fecha_local.month]
    anio = fecha_local.year
    hora = fecha_local.strftime("%H:%M")
    return f"{dia} {mes} {anio} {hora}"


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
    return render(request, 'tratamientos/lista_tratamientos.html', {'results': resultados})


@login_required
def buscar_tratamientos(request):
    parametro = request.GET.get('q', '')
    page_number = request.GET.get('page', 1)

    if parametro:
        tratamientos = Tratamiento.objects.filter(
            descripcion__icontains=parametro
        ).order_by("descripcion")
    else:
        tratamientos = Tratamiento.objects.all().order_by("descripcion")

    paginator = Paginator(tratamientos, 10)
    page_obj = paginator.get_page(page_number)

    data = [{
        "id": p.pk,
        "descripcion": p.descripcion,
        "precio": p.precio,
        "fecha": formatear_fecha(p.fecha),
        "usuario": p.usuario.username

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
def crear_tratamiento(request):
    if request.method == 'POST':
        form = TratamientoForm(request.POST)
        if form.is_valid():
            try:
                tratamiento = form.save(commit=False)
                tratamiento.usuario = request.user 
                tratamiento.save()
                return redirect('listar_tratamientos')
            except IntegrityError:
                messages.warning(request, "Ya existe un tratamiento con esa descripcion")

    else:
        form = TratamientoForm()
    return render(request, 'tratamientos/crear_tratamiento.html', {'form': form, 'accion': 'Crear'})


@login_required
def editar_tratamiento(request, pk):
    tratamiento = get_object_or_404(Tratamiento, pk=pk)
    if request.method == 'POST':
        form = TratamientoForm(request.POST, instance=tratamiento)
        if form.is_valid():
            try:
                tratamiento = form.save(commit=False)
                tratamiento.usuario = request.user 
                tratamiento.save()
                return redirect('listar_tratamientos')
            except IntegrityError:
                messages.warning(request, "Ya existe un tratamiento con esa descripcion")
    else:
        form = TratamientoForm(instance=tratamiento)
    return render(request, 'tratamientos/crear_tratamiento.html', {'form': form, 'accion': 'Editar'})


# Create your views here.
