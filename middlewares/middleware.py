

from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin

EXCLUDED_PATHS = ['/login/', '/admin/']

class UsuarioActivoMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path in EXCLUDED_PATHS:
            return None
        if request.user.is_authenticated and not request.user.is_active:
            return render(request, 'usuario_inactivo.html')
        return None
