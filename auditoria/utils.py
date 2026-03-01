from .models import Auditoria

def registrar_auditoria(usuario, accion, caso=None):
    Auditoria.objects.create(
        usuario=usuario,
        accion=accion,
        caso=caso
    )