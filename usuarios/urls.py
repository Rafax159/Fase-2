from django.urls import path
from . import views
from .views import seleccionar_rol

urlpatterns = [
    path('', seleccionar_rol, name='inicio'),
    path('crear/', views.crear_usuario, name='crear_usuario'),
    path('listar/', views.listar_usuarios, name='listar_usuarios'),
]