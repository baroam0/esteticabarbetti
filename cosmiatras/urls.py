

from django.urls import path
from . import views

urlpatterns = [
    path('lista', views.listar_cosmiatra, name='listar_cosmiatra'),
    path('crear/', views.crear_cosmiatra, name='crear_cosmiatra'),
    path('editar/<int:pk>', views.editar_cosmiatra, name='editar_cosmiatra'),
]

