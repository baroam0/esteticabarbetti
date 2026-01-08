

from django.urls import path
from . import views

urlpatterns = [
    path('cosmiatras', views.reporte_cosmiatra, name='reporte_cosmiatra')
]
