

from django.urls import path
from . import views

urlpatterns = [
    path('lista/', views.listar_cosmiatra, name='listar_cosmiatra'),
    path('crear/', views.crear_cosmiatra, name='crear_cosmiatra'),
    path('editar/<int:pk>', views.editar_cosmiatra, name='editar_cosmiatra'),

    path('cosmetologa/lista/', views.listar_cosmetologa, name='listar_cosmetologa'),
    path('cosmetologa/crear/', views.crear_cosmetologa, name='crear_cosmetologa'),
    path('cosmetologa/editar/<int:pk>', views.editar_cosmetologa, name='editar_cosmetologa'),
]

