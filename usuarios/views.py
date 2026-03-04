from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CrearUsuarioForm
from .models import Usuario

@login_required
def crear_usuario(request):

    # Solo administrador
    if not request.user.is_admin():
        return redirect('listar_casos')

    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = CrearUsuarioForm()

    return render(request, 'usuarios/crear_usuario.html', {
        'form': form
    })

@login_required
def listar_usuarios(request):

    if not request.user.is_admin():
        return redirect('listar_casos')

    usuarios = Usuario.objects.filter(rol='INVESTIGADOR')

    return render(request, 'usuarios/listar.html', {
        'usuarios': usuarios
    })

def seleccionar_rol(request):
    return render(request, 'usuarios/seleccionar_rol.html')