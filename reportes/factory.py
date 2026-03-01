from casos.models import Caso
from django.db.models import Count


class ReporteBase:
    def generar(self):
        raise NotImplementedError


class ReporteEmpresas(ReporteBase):

    def generar(self):
        return (
            Caso.objects
            .values('area_apoyo') 
            .annotate(total=Count('id'))
            .order_by('-total')
        )


class ReporteInvestigadores(ReporteBase):

    def generar(self):
        return (
            Caso.objects
            .values('investigador__username')
            .annotate(total=Count('id'))
            .order_by('-total')
        )


class ReporteFactory:

    @staticmethod
    def crear_reporte(tipo):

        if tipo == "empresas":
            return ReporteEmpresas()

        elif tipo == "investigadores":
            return ReporteInvestigadores()

        else:
            raise ValueError("Tipo de reporte no válido")