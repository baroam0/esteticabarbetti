
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ProductoForm
from .models import Producto, HistorialProducto


@login_required
def listar_productos(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        productos =  Producto.objects.filter(descripcion__contains=parametro)
    else:
        productos =  Producto.objects.all().order_by("descripcion")
    paginador = Paginator(productos, 15)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)

    return render(request, 'productos/lista_productos.html', {'resultados': resultados})


@login_required
def buscar_producto(request):
    parametro = request.GET.get('q', '')
    productos = Producto.objects.filter(descripcion__icontains=parametro).order_by("descripcion")

    data = []
    for p in productos:
        data.append({
            "id": p.pk,
            "descripcion": p.nombre,
            "precion": p.edad(),
            "stock": p.edad(),
        })
    return JsonResponse(data, safe=False)


@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.usuario = request.user 
            producto.save()

            HistorialProducto.objects.create(
                producto=producto,
                usuario=request.user,
                precio_registrado=producto.precio,
                stock_registrado=producto.stock,
                accion='CREADO'
            )

            return redirect('listar_productos')
    else:
        form = ProductoForm()
    return render(request, 'productos/crear_producto.html', {'form': form, 'accion': 'Crear'})


@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            producto_modificado = form.save()

            HistorialProducto.objects.create(
                producto=producto_modificado,
                usuario=request.user,
                precio_registrado=producto_modificado.precio,
                stock_registrado=producto_modificado.stock,
                accion='EDITADO'
            )
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/crear_producto.html', {'form': form, 'accion': 'Editar'})


@login_required
def listar_historial(request):
    productos =  Producto.objects.all().order_by("descripcion")
    paginador = Paginator(productos, 15)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)

    return render(request, 'productos/lista_productos.html', {'resultados': resultados})

# Create your views here.
