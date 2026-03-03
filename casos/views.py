from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Caso
from usuarios.models import Usuario
from auditoria.utils import registrar_auditoria
from auditoria.models import Auditoria
from django.utils import timezone
from datetime import timedelta
from .factory import CasoFactory
from .forms import CasoForm
from django.shortcuts import get_object_or_404, redirect
from .forms import CambiarEstatusForm

@login_required
def listar_casos(request):
    modo = request.GET.get('modo', None)

    if request.user.is_admin():
        casos = Caso.objects.all()
    else:
        casos = Caso.objects.filter(investigador=request.user)

    hoy = timezone.now()

    for caso in casos:
        dias = (hoy - caso.fecha_creacion).days

        if dias >= 10:
            caso.nivel_alarma = "critico"
        elif dias >= 5:
            caso.nivel_alarma = "advertencia"
        else:
            caso.nivel_alarma = "normal"

    return render(request, 'casos/listar.html', {
        'casos': casos,
        'modo': modo
    })

@login_required
def crear_caso(request):
    if request.method == 'POST':
        form = CasoForm(request.POST, request.FILES)

        if form.is_valid():

            caso = CasoFactory.crear_caso(
                form.cleaned_data,
                request.user
            )

            registrar_auditoria(
                request.user,
                f"Creó el caso {caso.id_caso}",
                caso
            )

            return redirect('listar_casos')

    else:
        form = CasoForm()

    return render(request, 'casos/crear.html', {
        'form': form
    })


@login_required
def asignar_investigador(request, caso_id):
    if not request.user.is_admin():
        return redirect('listar_casos')

    caso = get_object_or_404(Caso, id=caso_id)
    investigadores = Usuario.objects.filter(rol='INV')

    if request.method == 'POST':
        investigador_id = request.POST['investigador']
        investigador = Usuario.objects.get(id=investigador_id)
        caso.investigador = investigador
        caso.estatus = 'ASIGNADO'
        caso.save()

        registrar_auditoria(
            request.user,
            f"Asignó investigador al caso {caso.id_caso}",
            caso
        )
        return redirect('listar_casos')

    return render(request, 'casos/asignar.html', {
        'caso': caso,
        'investigadores': investigadores
    })


@login_required
def detalle_caso(request, caso_id):

    caso = get_object_or_404(Caso, id=caso_id)

    # Si es investigador, solo puede ver los suyos
    if request.user.is_investigador() and caso.investigador != request.user:
        return redirect('listar_casos')

    return render(request, 'casos/detalle.html', {
        'caso': caso
    })

@login_required
def cerrar_caso(request, caso_id):
    caso = get_object_or_404(Caso, id=caso_id)

    # Solo admin o investigador asignado
    if request.user.is_investigador() and caso.investigador != request.user:
        return redirect('listar_casos')
    
    if caso.estatus == 'CERRADO':
        return redirect('detalle_caso', caso_id=caso.id)

    if request.method == 'POST':
        observaciones = request.POST['observaciones']
        conclusiones = request.POST['conclusiones']
        recomendaciones = request.POST['recomendaciones']

        # Validación obligatoria (RF-05)
        if not observaciones or not conclusiones or not recomendaciones:
            return render(request, 'casos/cerrar.html', {
                'caso': caso,
                'error': 'Todos los campos son obligatorios'
            })

        caso.observaciones = observaciones
        caso.conclusiones = conclusiones
        caso.recomendaciones = recomendaciones
        caso.estatus = 'CERRADO'
        caso.save()

        registrar_auditoria(
            request.user,
            f"Cerró el caso {caso.id_caso}",
            caso
        )

        return redirect('detalle_caso', caso_id=caso.id)

    return render(request, 'casos/cerrar.html', {'caso': caso})


@login_required
def reabrir_caso(request, caso_id):
    caso = get_object_or_404(Caso, id=caso_id)

    # Solo admin o investigador asignado
    if request.user.is_investigador() and caso.investigador != request.user:
        return redirect('listar_casos')

    # Solo si está cerrado
    if caso.estatus != 'CERRADO':
        return redirect('detalle_caso', caso_id=caso.id)

    caso.estatus = 'ASIGNADO'
    caso.save()

    registrar_auditoria(
        request.user,
        f"Reabrió el caso {caso.id_caso}",
        caso
    )

    return redirect('detalle_caso', caso_id=caso.id)

@login_required
def modificar_caso(request, caso_id):

    if not request.user.is_admin():
        return redirect('listar_casos')

    caso = get_object_or_404(Caso, id=caso_id)

    if request.method == 'POST':
        form = CasoForm(request.POST, request.FILES, instance=caso)

        if form.is_valid():
            form.save()

            registrar_auditoria(
                request.user,
                f"Modificó el caso {caso.id_caso}",
                caso
            )

            return redirect('detalle_caso', caso_id=caso.id)

    else:
        form = CasoForm(instance=caso)

    return render(request, 'casos/crear.html', {
        'form': form
    })

@login_required
def eliminar_caso(request, caso_id):

    if not request.user.is_admin():
        return redirect('listar_casos')

    caso = get_object_or_404(Caso, id=caso_id)

    if request.method == 'POST':

        registrar_auditoria(
            request.user,
            f"Eliminó el caso {caso.id_caso}",
            caso
        )

        caso.delete()
        return redirect('listar_casos')

    return render(request, 'casos/eliminar.html', {
        'caso': caso
    })

@login_required
def cambiar_estatus(request, caso_id):

    caso = get_object_or_404(Caso, id=caso_id)

    if request.method == 'POST':
        form = CambiarEstatusForm(request.POST, instance=caso)

        if form.is_valid():
            form.save()
            return redirect('detalle_caso', caso_id=caso.id)

    else:
        form = CambiarEstatusForm(instance=caso)

    return render(request, 'casos/cambiar_estatus.html', {
        'form': form,
        'caso': caso
    })

def obtener_alarmas(usuario):
    alarmas = []

    hoy = timezone.now().date()

    if usuario.rol == 'ADMIN':

        sin_asignar = Caso.objects.filter(estatus='Abierto').count()
        if sin_asignar > 0:
            alarmas.append(f"Hay {sin_asignar} casos sin asignar")

    vencidos = Caso.objects.filter(
        fecha_inicio__isnull=False
    )

    for caso in vencidos:
        if caso.fecha_inicio and caso.duracion:
            fecha_limite = caso.fecha_inicio + timedelta(days=caso.duracion)
            if fecha_limite < hoy:
                alarmas.append(f"El caso {caso.id_caso} está vencido")

    return alarmas

@login_required
def mis_casos(request):
    casos = Caso.objects.filter(investigador=request.user)
    return render(request, 'casos/listar.html', {
        'casos': casos
    })

    