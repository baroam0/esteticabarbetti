
from django.urls import path
from .views import TurnoListView, TurnoCreateView, TurnoUpdateView, TurnoEventsView

urlpatterns = [
    path('lista/', TurnoListView.as_view(), name='turno_list'),
    path('nuevo/', TurnoCreateView.as_view(), name='turno_create'),
    path('editar/<int:pk>', TurnoUpdateView.as_view(), name='turno_update'),
    path('api/turnos/', TurnoEventsView.as_view(), name='turno_events'),
]
