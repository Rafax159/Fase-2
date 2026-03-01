from django.utils import timezone
from datetime import timedelta
from .models import Caso

def alarmas_globales(request):

    if not request.user.is_authenticated:
        return {}

    alarmas = []
    hoy = timezone.now().date()

    # Admin: casos abiertos
    if request.user.is_staff:
        sin_asignar = Caso.objects.filter(estatus='Abierto').count()
        if sin_asignar > 0:
            alarmas.append(f"Hay {sin_asignar} casos sin asignar")

    # Casos vencidos
    casos = Caso.objects.filter(fecha_inicio__isnull=False)

    for caso in casos:
        if hasattr(caso, 'duracion_dias') and caso.fecha_inicio and caso.duracion_dias:
            fecha_limite = caso.fecha_inicio + timedelta(days=caso.duracion_dias)
            if fecha_limite < hoy:
                alarmas.append(f"El caso {caso.id_caso} está vencido")

    return {
        'alarmas': alarmas
    }