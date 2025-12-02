

from django.urls import path
from . import views

urlpatterns = [
    path('lista/<int:pk>', views.listar_historiasclinicas, name='listar_historiasclinicas'),
    path('crear/<int:pk>', views.crear_historiaclinica, name='crear_historiaclinica'),
    path('editar/<int:pk>', views.editar_historiaclinica, name='editar_historiaclinica'),

     # Nueva: detalle de historia clínica con imágenes
    path('detalle/<int:pk>', views.detalle_historia, name='detalle_historia'),

    # Opcional: agregar imágenes a una historia clínica ya existente
    #path('agregar-imagenes/<int:pk>', views.agregar_imagenes_historia, name='agregar_imagenes_historia'),
]


