from django.db import models
from django.core.validators import FileExtensionValidator

class Caso(models.Model):

    id_caso = models.CharField(max_length=50)
    nro_expediente = models.CharField(max_length=50)

    investigador = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    fecha_inicio = models.DateField()

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    dias = models.IntegerField()
    mes = models.CharField(max_length=20)

    movil_afectado = models.CharField(max_length=100)
    TIPOS_CASO = [
    ('GESTION', 'Gestión'),
    ('RECLAMO', 'Reclamo'),
    ('CASO', 'Caso'),
    ]

    tipo_caso = models.CharField(
        max_length=20,
        choices=TIPOS_CASO
    )

    tipo_irregularidad = models.CharField(max_length=100)
    subtipo_irregularidad = models.CharField(max_length=100)

    objetivo_agraviado = models.CharField(max_length=200)
    incidencia = models.TextField()

    duracion_dias = models.IntegerField()
    descripcion_modus_operandi = models.TextField()
    area_apoyo = models.CharField(max_length=200)

    deteccion_procedencia = models.TextField()
    diagnostico = models.TextField()
    actuaciones = models.TextField()

    conclusiones = models.TextField()
    observaciones = models.TextField()

    soporte = models.FileField(
        upload_to='soportes/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'jpg', 'jpeg', 'png']
            )
        ],
        blank=True,
        null=True
    )

    ESTATUS = [
        ('ABIERTO', 'Abierto'),
        ('ASIGNADO', 'Asignado'),
        ('CERRADO', 'Cerrado'),
    ]

    estatus = models.CharField(max_length=20, choices=ESTATUS)