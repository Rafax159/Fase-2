from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CrearUsuarioForm
from .models import Usuario
from django.contrib.auth.views import LoginView
from django.contrib import messages

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        user = form.get_user()
        rol = self.request.GET.get('rol')

        # Validación según rol seleccionado
        if rol == 'admin' and not user.is_staff:
            messages.error(self.request, "Estas credenciales no pertenecen a un administrador.")
            return redirect(f"{self.request.path}?rol=admin")

        if rol == 'investigador' and user.is_staff:
            messages.error(self.request, "Estas credenciales no pertenecen a un investigador.")
            return redirect(f"{self.request.path}?rol=investigador")

        return super().form_valid(form)

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