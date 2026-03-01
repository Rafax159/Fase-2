from .models import EquipoRobado, PersonalSancionado


class RegistroFactory:

    @staticmethod
    def crear_registro(tipo, datos):

        if tipo == "equipo":
            return EquipoRobado.objects.create(
                serial=datos.get("serial"),
                tipo_equipo=datos.get("tipo_equipo"),
                marca=datos.get("marca"),
                modelo=datos.get("modelo"),
                observaciones=datos.get("observaciones"),
            )

        elif tipo == "personal":
            return PersonalSancionado.objects.create(
                cedula=datos.get("cedula"),
                nombre=datos.get("nombre"),
                apellido=datos.get("apellido"),
                empresa=datos.get("empresa"),
                estado=datos.get("estado"),
            )

        else:
            raise ValueError("Tipo de registro no válido")