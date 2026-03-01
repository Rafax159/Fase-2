from django.db import models


class EquipoRobado(models.Model):

    serial = models.CharField(max_length=100, unique=True)
    tipo_equipo = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    observaciones = models.TextField(blank=True)

    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.serial} - {self.marca} {self.modelo}"


class PersonalSancionado(models.Model):

    ESTADO_CHOICES = (
        ('AMONESTADO', 'Amonestado'),
        ('DESINCORPORADO', 'Desincorporado'),
    )

    cedula = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    empresa = models.CharField(max_length=150)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)

    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"