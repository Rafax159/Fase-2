from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class CrearUsuarioForm(UserCreationForm):

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'rol']