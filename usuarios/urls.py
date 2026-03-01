from django.urls import path
from . import views

urlpatterns = [
    path('crear/', views.crear_usuario, name='crear_usuario'),
    path('listar/', views.listar_usuarios, name='listar_usuarios'),
]