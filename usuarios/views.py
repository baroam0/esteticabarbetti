
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def listar_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'usuarios/lista_usuarios2.html', {'usuarios': usuarios})


@login_required
def crear_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe.")
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Usuario creado correctamente.")
            return redirect('listar_usuarios')

    return render(request, 'usuarios/crear.html')

@login_required
def editar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        usuario.username = request.POST.get('username')
        usuario.email = request.POST.get('email')
        usuario.save()
        messages.success(request, "Usuario actualizado correctamente.")
        return redirect('listar_usuarios')

    return render(request, 'usuarios/editar.html', {'usuario': usuario})


@login_required
def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    usuario.delete()
    messages.success(request, "Usuario eliminado correctamente.")
    return redirect('listar_usuarios')


# Create your views here.
