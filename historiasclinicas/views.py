

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from pacientes.models import Paciente
from .forms import HistoriaClinicaForm, ImagenHistoriaClinicaForm
from .models import HistoriaClinica, ImagenHistoriaClinica


@login_required
def listar_historiasclinicas(request, pk):
    paciente = Paciente.objects.get(pk=pk)
    historiasclinicas = HistoriaClinica.objects.filter(paciente=paciente).order_by('fecha')
    return render(
        request, 
        'historiasclinicas/lista_historiaclinica.html', 
        {
            'historiasclinicas': historiasclinicas,
            'paciente': paciente
        }
    )

"""
@login_required
def crear_historiaclinica(request, pk):
    paciente = Paciente.objects.get(pk=pk)
    if request.method == 'POST':
        form = HistoriaClinicaForm(request.POST)
        if form.is_valid():
            historiaclinica = form.save(commit=False)
            historiaclinica.paciente = paciente
            historiaclinica.responsable = request.user 
            historiaclinica.save()
            form.save()
            return redirect('listar_historiasclinicas', pk=pk)
    else:
        form = HistoriaClinicaForm()
    
    return render(request, 'historiasclinicas/crear_historiaclinica.html', {'form': form})
"""

@login_required
def crear_historiaclinica(request, pk):
    paciente = Paciente.objects.get(pk=pk)
    if request.method == 'POST':
        form_historiaclinica = HistoriaClinicaForm(request.POST)
        form_imagenes = ImagenHistoriaClinicaForm(request.POST, request.FILES)

        if form_historiaclinica.is_valid():
            historiaclinica = form_historiaclinica.save(commit=False)
            historiaclinica.paciente = paciente
            historiaclinica.responsable = request.user 
            historiaclinica.save()

            # Guardar múltiples imágenes
            imagenes = request.FILES.getlist('imagen')
            for img in imagenes:
                ImagenHistoriaClinica.objects.create(historiaclinica=historiaclinica, imagen=img)

            #return redirect('detalle_historia', pk=historia.pk)
            return redirect('listar_historiasclinicas', pk=pk)
    else:
        form_historiaclinica = HistoriaClinicaForm()
        form_imagenes = ImagenHistoriaClinicaForm()

    return render(request, 'historiasclinicas/crear_historiaclinica.html', {
        'accion': "Crear",
        'form': form_historiaclinica,
        'form_imagenes': form_imagenes,
        'paciente': paciente
    })

"""
def agregar_imagenes_historia(request, pk):
    historia = get_object_or_404(HistoriaClinica, pk=pk)

    if request.method == 'POST':
        form_imagenes = ImagenHistoriaClinicaForm(request.POST, request.FILES)
        if form_imagenes.is_valid():
            imagenes = request.FILES.getlist('imagen')
            for img in imagenes:
                ImagenHistoriaClinica.objects.create(historia=historia, imagen=img)
            return redirect('detalle_historia', pk=historia.pk)
    else:
        form_imagenes = ImagenHistoriaClinicaForm()

    return render(request, 'historias/agregar_imagenes.html', {
        'historia': historia,
        'form_imagenes': form_imagenes
    })
"""


def detalle_historia(request, pk):
    historia = get_object_or_404(HistoriaClinica, pk=pk)
    imagenes = historia.imagenes.all()
    return render(request, 'historias/detalle_historia.html', {
        'historia': historia,
        'imagenes': imagenes
    })




@login_required
def editar_historiaclinica(request, pk):
    historia = get_object_or_404(HistoriaClinica, pk=pk)

    if request.method == 'POST':
        form_historia = HistoriaClinicaForm(request.POST, instance=historia)
        if form_historia.is_valid():
            form_historia.save()
            return redirect('detalle_historia', pk=historia.pk)
    else:
        form_historia = HistoriaClinicaForm(instance=historia)

    return render(request, 'historias/editar_historia.html', {
        'form_historia': form_historia,
        'historia': historia
    })



"""

def editar_historiaclinica(request, pk):
    historiaclinica = get_object_or_404(HistoriaClinica, pk=pk)
    
    if request.method == "POST":
        print("por el post")
        form = HistoriaClinicaForm(request.POST, instance=historiaclinica)
        if form.is_valid():
            fomulariohistoriaclinica = form.save(commit=False)
            fomulariohistoriaclinica.responsable = request.user
            fomulariohistoriaclinica.save()
            #form.save()
            print(historiaclinica.paciente.pk)
            return redirect('listar_historiasclinicas', pk=historiaclinica.paciente.pk)
            
    else:
        form = HistoriaClinicaForm(instance=historiaclinica)
    
    return render(
        request, 
        "historiasclinicas/crear_historiaclinica.html", 
        {
            "accion": "Editar", 
            "form": form, 
            "historiaclinica": historiaclinica
        }
    )
"""


def detalle_historia(request, pk):
    historia = get_object_or_404(HistoriaClinica, pk=pk)
    imagenes = historia.imagenes.all()
    return render(request, 'historias/detalle_historia.html', {
        'historia': historia,
        'imagenes': imagenes
    })


# Create your views here.
