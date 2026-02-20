
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.urls import reverse

from pacientes.models import Paciente
from .forms import HistoriaClinicaForm, ImagenMultipleForm
from .models import HistoriaClinica, ImagenHistoriaClinica

from turnos.models import Turno, TurnoProducto


"""
@login_required
def listar_historiasclinicas(request, pk):
    paciente = Paciente.objects.get(pk=pk)
    historiasclinicas = HistoriaClinica.objects.filter(paciente=paciente).order_by('-fecha')
    turnos = Turno.objects.filter(
        sexo=paciente.sexo, numerodocumento=paciente.numerodocumento
    ).order_by('-fecha_hora')

    return render(
        request, 
        'historiasclinicas/lista_historiaclinica.html', 
        {
            'historiasclinicas': historiasclinicas,
            'paciente': paciente,
            'turnos': turnos
        }
    )
"""

@login_required
def listar_historiasclinicas(request, pk): 
    paciente = Paciente.objects.get(pk=pk) 
    historiasclinicas = HistoriaClinica.objects.filter(
        paciente=paciente).order_by('-fecha') 
    
    turnos = Turno.objects.filter(
        sexo=paciente.sexo, numerodocumento=paciente.numerodocumento
    ).order_by('-fecha_hora') 
    
    lista_turnos = [] 
    for turno in turnos: 
        productos = TurnoProducto.objects.filter(turno=turno)
        
        lista_turnos.append(
            {
                "cosmiatra": turno.cosmetologa,
                "fecha_hora": turno.fecha_hora, 
                "tratamiento": " - ".join([t.descripcion for t in turno.tratamientos.all()]),
                "producto": " - ".join([p.producto.descripcion for p in productos]),
            }
        ) 

    return render(
        request, 
        'historiasclinicas/lista_historiaclinica.html', 
        {
            'historiasclinicas': historiasclinicas,
            'paciente': paciente,
            'turnos': lista_turnos
        }
    )


@login_required
def crear_historiaclinica(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)

    if request.method == "POST":
        form = HistoriaClinicaForm(request.POST)
        imagenes_form = ImagenMultipleForm(request.POST, request.FILES)

        if form.is_valid() and imagenes_form.is_valid():
            historia = form.save(commit=False)
            historia.paciente = paciente
            historia.responsable = request.user
            historia.save()
           
            for img in request.FILES.getlist('imagenes[]'):
                ImagenHistoriaClinica.objects.create(
                    historiaclinica=historia,
                    imagen=img
                )

            return redirect('editar_historiaclinica', pk=historia.pk)

    else:
        form = HistoriaClinicaForm()
        imagenes_form = ImagenMultipleForm()

    return render(
        request,
        "historiasclinicas/crear_historiaclinica.html",
        {
            "accion": "Crear",
            "form": form,
            "imagenes_form": imagenes_form,
            "paciente": paciente
        }
    )


@login_required
def editar_historiaclinica(request, pk):
    historia = get_object_or_404(HistoriaClinica, pk=pk)
    paciente = historia.paciente

    if request.method == "POST":
        form = HistoriaClinicaForm(request.POST, instance=historia)
        imagenes_form = ImagenMultipleForm(request.POST, request.FILES)

        if form.is_valid() and imagenes_form.is_valid():
            historia = form.save(commit=False)
            historia.responsable = request.user
            historia.save()

            # Obtener archivos enviados
            imagenes = request.FILES.getlist('imagenes[]')

            for img in imagenes:
                ImagenHistoriaClinica.objects.create(
                    historiaclinica=historia,
                    imagen=img
                )

            return redirect('editar_historiaclinica', pk=historia.pk)

    else:
        form = HistoriaClinicaForm(instance=historia)
        imagenes_form = ImagenMultipleForm()

    imagenes_existentes = historia.imagenes.all()

    return render(
        request,
        "historiasclinicas/crear_historiaclinica.html",
        {
            "accion": "Editar",
            "form": form,
            "imagenes_form": imagenes_form,
            "paciente": paciente,
            "historia": historia,
            "imagenes_existentes": imagenes_existentes
        }
    )

def eliminar_imagen(request, pk):
    if request.method == "POST":
        ImagenHistoriaClinica.objects.filter(pk=pk).delete()
        return JsonResponse({"ok": True})


def eliminar_historiaclinica(request, pk):
    historiaclinica = get_object_or_404(HistoriaClinica, pk=pk)
    imagenhistoriaclinica = ImagenHistoriaClinica.objects.filter(historiaclinica=historiaclinica.pk)

    if request.method == "POST":
        historiaclinica.delete()
        return redirect(
            reverse(
                "listar_historiasclinicas", 
                args=[historiaclinica.paciente.id]
            )
        )

    return render(
        request, 
        "historiasclinicas/eliminar_historiaclinica.html", 
        {
            "historiaclinica": historiaclinica,
            "imagenhistoriaclinica":imagenhistoriaclinica
        }
    )


# Create your views here.
