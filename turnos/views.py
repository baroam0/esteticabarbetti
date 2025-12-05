
from datetime import datetime
from django.views.generic import ListView, CreateView, UpdateView
from django.views import View
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Turno
from .forms import TurnoForm

from cosmiatras.models import Cosmetologa

class TurnoListView(ListView):
    model = Turno
    template_name = 'turnos/turno_list.html'
    context_object_name = 'turnos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cosmetologas'] = Cosmetologa.objects.all()
        return context

class TurnoCreateView(CreateView):
    model = Turno
    form_class = TurnoForm
    template_name = 'turnos/turno_form.html'
    success_url = reverse_lazy('turno_list')

    def get_initial(self):
        initial = super().get_initial()
        fecha = self.request.GET.get('fecha')
        if fecha:
            try:
                dt = datetime.strptime(fecha, "%Y-%m-%d").replace(hour=9, minute=0)
                initial['fecha_hora'] = dt.strftime("%Y-%m-%dT%H:%M")
            except ValueError:
                pass
        return initial


class TurnoUpdateView(UpdateView):
    model = Turno
    form_class = TurnoForm
    template_name = 'turnos/turno_form.html'
    success_url = reverse_lazy('turno_list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class TurnoEventsView(View):
    def get(self, request, *args, **kwargs):
        cosmetologa_id = request.GET.get('cosmetologa')  # parámetro en la URL
        turnos = Turno.objects.select_related('cosmetologa').prefetch_related('tratamientos')

        if cosmetologa_id:
            turnos = turnos.filter(cosmetologa_id=cosmetologa_id)

        eventos = []
        for turno in turnos:
            eventos.append({
                "id": turno.id,
                "title": f"{turno.cosmetologa.nombre} - {', '.join([t.descripcion for t in turno.tratamientos.all()])}",
                "start": turno.fecha_hora.isoformat(),
                "url": f"/turnos/{turno.id}/editar/"
            })
        return JsonResponse(eventos, safe=False)


# Create your views here.
