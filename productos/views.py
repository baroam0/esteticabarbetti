
from django.db import IntegrityError
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

    return render(request, 'productos/lista_productos.html', {'results': resultados})


@login_required
def buscar_productos(request):
    parametro = request.GET.get('q', '')
    page_number = request.GET.get('page', 1)

    if parametro:
        productos = Producto.objects.filter(
            descripcion__icontains=parametro
        ).order_by("descripcion")
    else:
        productos =  Producto.objects.all().order_by("descripcion")

    paginator = Paginator(productos, 15)
    page_obj = paginator.get_page(page_number)

    data = [{
        "id": p.pk,
        "descripcion": p.descripcion,
        "precio": p.precio,
        "stock": p.stock,
        "fecha_actualizacion": p.fecha_actualizacion.strftime("%d %b. %Y %H:%M"),
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
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():

            try:
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
            except IntegrityError:
                messages.warning(request, "Ya existe un producto con esa descripcion")
    else:
        form = ProductoForm()
    return render(request, 'productos/crear_producto.html', {'form': form, 'accion': 'Crear'})


@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            try:
                producto_modificado = form.save(commit=False)
                producto.usuario=request.user
                producto.save()
                HistorialProducto.objects.create(
                    producto=producto_modificado,
                    usuario=request.user,
                    precio_registrado=producto_modificado.precio,
                    stock_registrado=producto_modificado.stock,
                    accion='EDITADO'
                )
                return redirect('listar_productos')
            except IntegrityError:
                messages.warning(request, "Ya existe un producto con esa descripcion")

    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/crear_producto.html', {'form': form, 'accion': 'Editar'})


@login_required
def listar_historial(request, pk):
    producto =  Producto.objects.get(pk=pk)
    historial = HistorialProducto.objects.filter(producto=producto).order_by("-fecha_modificacion")
    paginador = Paginator(historial, 15)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)

    return render(
        request, 
        'productos/lista_historial.html', 
        {
            'results': resultados,
            'producto': producto.descripcion
        }
    )

# Create your views here.

