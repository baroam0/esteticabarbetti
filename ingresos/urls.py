

from django.urls import path
from . import views

urlpatterns = [
    path('ingresos/', views.ingresos_view , name='ingresos'),
    path('ingresos2/', views.ingresos_view2 , name='ingresos2'),
    path('ingresos3/', views.ingresos_view3 , name='ingresos3'),
    path('listarcategorias/', views.listar_categorias , name='listar_categorias'),
    path('crearcategoria/', views.crear_categoria , name='crear_categoria'),
    path('editarcategoria/<int:pk>', views.editar_categoria , name='editar_categoria'),
    path('editarcategoria/<int:pk>', views.editar_categoria , name='editar_categoria'),
    path('senias/', views.senias_view , name='senias_view'),
]
