

from django.urls import path
from . import views

urlpatterns = [
    path('ingresos/', views.ingresos_view , name='ingresos'),
    path('ingresos2/', views.ingresos_view2 , name='ingresos2'),
    path('ingresos3/', views.ingresos_view3 , name='ingresos3'),
]
