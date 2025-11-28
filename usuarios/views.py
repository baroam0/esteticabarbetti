
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .forms import UsuarioForm


@login_required
def listar_usuarios(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        usuarios = User.objects.filter(username__contains=parametro)
    else:
        usuarios = User.objects.all().order_by("username")
    paginador = Paginator(usuarios, 15)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    usuarios = paginador.get_page(page)
    return render(request, 'usuarios/lista_usuarios2.html', {'usuarios': usuarios})


@login_required
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']

            if User.objects.filter(username=username).exists():
                messages.error(request, "El nombre de usuario ya existe.")
            else:
                User.objects.create_user(
                    username=username, 
                    first_name=first_name, 
                    last_name=last_name, 
                    password=password
                )
                messages.success(request, "Usuario creado correctamente.")
                return redirect('listar_usuarios')
    else:
        form = UsuarioForm()

    return render(
        request, 
        'usuarios/crear_usuario.html', 
        {
            'accion': 'Crear',
            'form': form
        }
    )


@login_required
def editar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save(commit=False)
            if form.cleaned_data.get('password'):
                usuario.set_password(form.cleaned_data['password'])
            usuario.save()

            if usuario == request.user:
                update_session_auth_hash(request, usuario)

            messages.success(request, "Usuario actualizado correctamente.")
            return redirect('home')
    else:
        form = UsuarioForm(instance=usuario)

    return render(
        request,
        'usuarios/crear_usuario.html',
        {
            'accion': 'Editar',
            'form': form
        }
    )



@login_required
def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    usuario.delete()
    messages.success(request, "Usuario eliminado correctamente.")
    return redirect('homes')


# Create your views here.
