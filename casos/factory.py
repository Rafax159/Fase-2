from .models import Caso

class CasoFactory:

    @staticmethod
    def crear_caso(data, usuario):

        caso = Caso(**data)

        if usuario.is_admin():
            caso.estatus = 'ASIGNADO'
            caso.investigador = data.get('investigador')
        else:
            caso.estatus = 'ABIERTO'
            caso.investigador = usuario

        caso.save()
        return caso
