

from django.urls import path
from . import views

urlpatterns = [
    path('lista', views.listar_pacientes, name='listar_pacientes'),
    path('buscar', views.buscar_pacientes, name='buscar_pacientes'),
    path('crear/', views.crear_paciente, name='crear_pacientes'),
    path('editar/<int:pk>', views.editar_paciente, name='editar_paciente'),
    path('eliminar/<int:pk>', views.eliminar_paciente, name='eliminar_paciente'),
    path('unificar', views.unificar_paciente, name='unificar_paciente'),
    path(
        'unificarbuscar', 
        views.unificar_buscar_pacientes, 
        name='unificar_buscar_pacientes'
    ),
    path('unificarpaciente/', views.unificar_proceso_paciente, name='unificar_proceso_paciente'),
]

