from django.urls import path
from . import views

urlpatterns = [
    path('', views.panel_reportes, name='panel_reportes'),
    path('<str:tipo>/', views.generar_reporte, name='generar_reporte'),
]