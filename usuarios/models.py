from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('INV', 'Investigador'),
    )

    rol = models.CharField(
        max_length=5,
        choices=ROLES,
        default='INV'
    )

    def is_admin(self):
        return self.rol == 'ADMIN' or self.is_superuser

    def is_investigador(self):
        return self.rol == 'INV'

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"