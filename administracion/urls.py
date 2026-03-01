from django.urls import path
from . import views

urlpatterns = [
    path('', views.panel_admin, name='panel_admin'),
    path('registrar-equipo/', views.registrar_equipo, name='registrar_equipo'),
    path('registrar-personal/', views.registrar_personal, name='registrar_personal'),
    path('equipos/', views.listar_equipos, name='listar_equipos'),
    path('personal/', views.listar_personal, name='listar_personal'),
]