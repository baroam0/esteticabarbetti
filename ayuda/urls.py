

from django.urls import path
from . import views

urlpatterns = [
    path('inicio', views.inicio, name='inicio'),
    path('tratamientos', views.tratamientos, name='tratamientos'),
    #path('crear/', views.crear_cosmiatra, name='crear_cosmiatra'),
    #path('editar/<int:pk>', views.editar_cosmiatra, name='editar_cosmiatra'),
]

