from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .factory import ReporteFactory


@login_required
def panel_reportes(request):

    # Solo investigador (no admin)
    if request.user.is_staff:
        return redirect('listar_casos')

    return render(request, 'reportes/panel_reportes.html')


@login_required
def generar_reporte(request, tipo):

    if request.user.is_staff:
        return redirect('listar_casos')

    factory = ReporteFactory()
    reporte = factory.crear_reporte(tipo)

    datos = reporte.generar()

    return render(request, f'reportes/reporte_{tipo}.html', {
        'datos': datos
    })