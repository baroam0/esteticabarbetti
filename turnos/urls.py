
from django.urls import path
from .views import (TurnoListView, TurnoCreateView, TurnoUpdateView, 
                    TurnoEventsView, listar_turnos, buscar_turnos, listar_tratamientos)

urlpatterns = [
    path('lista/', TurnoListView.as_view(), name='turno_list'),
    path('nuevo/', TurnoCreateView.as_view(), name='turno_create'),
    path('editar/<int:pk>', TurnoUpdateView.as_view(), name='turno_update'),
    path('api/turnos/', TurnoEventsView.as_view(), name='turno_events'),
    path('listar', listar_turnos, name='listar_turnos'),
    path('buscar', buscar_turnos, name='buscar_turnos'),
    path('tratamientos/historial/<int:pk>', listar_tratamientos, name='listar_tratamientos'),
]
