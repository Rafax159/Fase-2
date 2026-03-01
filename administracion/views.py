from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .factory import RegistroFactory


@login_required
def panel_admin(request):

    if not request.user.is_staff:
        return redirect('listar_casos')

    return render(request, 'administracion/panel_admin.html')


@login_required
def registrar_equipo(request):

    if not request.user.is_staff:
        return redirect('listar_casos')

    if request.method == 'POST':
        RegistroFactory.crear_registro("equipo", request.POST)
        return redirect('panel_admin')

    return render(request, 'administracion/registrar_equipo.html')


@login_required
def registrar_personal(request):

    if not request.user.is_staff:
        return redirect('listar_casos')

    if request.method == 'POST':
        RegistroFactory.crear_registro("personal", request.POST)
        return redirect('panel_admin')

    return render(request, 'administracion/registrar_personal.html')

from .models import EquipoRobado, PersonalSancionado


@login_required
def listar_equipos(request):

    if not request.user.is_staff:
        return redirect('listar_casos')

    equipos = EquipoRobado.objects.all().order_by('-fecha_registro')

    return render(request, 'administracion/listar_equipos.html', {
        'equipos': equipos
    })


@login_required
def listar_personal(request):

    if not request.user.is_staff:
        return redirect('listar_casos')

    personal = PersonalSancionado.objects.all().order_by('-fecha_registro')

    return render(request, 'administracion/listar_personal.html', {
        'personal': personal
    })