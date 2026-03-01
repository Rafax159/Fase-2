from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_casos, name='listar_casos'),
    path('crear/', views.crear_caso, name='crear_caso'),
    path('asignar/<int:caso_id>/', views.asignar_investigador, name='asignar_investigador'),
    path('detalle/<int:caso_id>/', views.detalle_caso, name='detalle_caso'),
    path('cerrar/<int:caso_id>/', views.cerrar_caso, name='cerrar_caso'),
    path('reabrir/<int:caso_id>/', views.reabrir_caso, name='reabrir_caso'),
    path('modificar/<int:caso_id>/', views.modificar_caso, name='modificar_caso'),
    path('eliminar/<int:caso_id>/', views.eliminar_caso, name='eliminar_caso'),
    path('cambiar-estatus/<int:caso_id>/', views.cambiar_estatus, name='cambiar_estatus'),
]
