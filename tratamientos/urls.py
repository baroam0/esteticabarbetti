

from django.urls import path
from . import views


urlpatterns = [
    path('lista', views.listar_tratamientos, name='listar_tratamientos'),
    path('buscar', views.buscar_tratamientos, name='buscar_tratamientos'),
    path('crear/', views.crear_tratamiento, name='crear_tratamiento'),
    path('editar/<int:pk>/', views.editar_tratamiento, name='editar_tratamiento'),   
]

