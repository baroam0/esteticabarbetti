
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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



# Create your views here.
