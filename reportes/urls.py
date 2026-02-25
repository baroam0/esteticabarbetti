

from django.urls import path
from . import views

urlpatterns = [
    path('cosmiatras/', views.reporte_cosmiatra, name='reporte_cosmiatra'),
    path('productos/', views.reporte_productos, name='reporte_productos'),
    path('graficotratamientos/', views.grafico_tratamientos, name='grafico_tratamientos')
]
