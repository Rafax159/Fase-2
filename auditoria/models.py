from django.db import models
from usuarios.models import Usuario
from casos.models import Caso

class Auditoria(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True
    )

    caso = models.ForeignKey(
        Caso,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    accion = models.CharField(max_length=200)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.fecha} - {self.usuario} - {self.accion}"