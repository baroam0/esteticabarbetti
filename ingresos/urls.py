

from django.urls import path
from . import views

urlpatterns = [
    path('ingresos', views.ingresos_view , name='ingresos'),
]
