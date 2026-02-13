

from django.urls import path
from . import views

urlpatterns = [
    path('lista/<int:pk>', views.listar_historiasclinicas, name='listar_historiasclinicas'),
    path('crear/<int:pk>', views.crear_historiaclinica, name='crear_historiaclinica'),
    path('editar/<int:pk>', views.editar_historiaclinica, name='editar_historiaclinica'),
    path("eliminar/<int:pk>", views.eliminar_historiaclinica, name="eliminar_historiaclinica"),
    path('api/imagen/eliminar/<int:pk>', views.eliminar_imagen, name='eliminar_imagen'),
]


