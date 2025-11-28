

from django.urls import path
from . import views

urlpatterns = [
    path('lista', views.listar_pacientes, name='listar_pacientes'),
    path('buscar', views.buscar_pacientes, name='buscar_pacientes'),
    #path('crear/', views.crear_usuario, name='crear_paciente'),
    #path('editar/<int:user_id>/', views.editar_usuario, name='editar_paciente'),
]

