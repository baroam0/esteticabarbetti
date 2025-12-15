
from datetime import datetime

from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .models import Turno
from .forms import TurnoForm

from cosmiatras.models import Cosmetologa
from productos.models import HistorialProducto

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

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        response = super().form_valid(form)
        
        productos_seleccionados = form.cleaned_data.get('productos')

        for producto in productos_seleccionados:
            if producto.stock <= 0:
                messages.error(self.request, f"El producto {producto.descripcion} no tiene stock disponible.")
                return redirect("turno_create")  # o donde corresponda

            producto.stock -= 1
            producto.save()

            HistorialProducto.objects.create(
                producto=producto,
                usuario=self.request.user,
                precio_registrado=producto.precio,
                stock_registrado=producto.stock,
                accion="TURNO",
                observaciones=f"Fecha del turno: {form.instance.fecha_hora.strftime('%d-%m-%Y %H:%M')}"
            )

        return response


class TurnoUpdateView(UpdateView):
    model = Turno
    form_class = TurnoForm
    template_name = 'turnos/turno_form.html'
    success_url = reverse_lazy('turno_list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user

        turno_original = Turno.objects.get(pk=self.object.pk)
        productos_antes = set(turno_original.productos.all())
        productos_despues = set(form.cleaned_data['productos'])

        productos_quitados = productos_antes - productos_despues
        productos_agregados = productos_despues - productos_antes

        for producto in productos_agregados:
            if producto.stock <= 0:
                messages.error(
                    self.request,
                    f"El producto {producto.descripcion} no tiene stock disponible."
                )
                return self.form_invalid(form)

        response = super().form_valid(form)

        for producto in productos_quitados:
            producto.stock += 1
            producto.save()

        for producto in productos_agregados:
            producto.stock -= 1
            producto.save()
        
        HistorialProducto.objects.create(
            producto=producto,
            usuario=self.request.user,
            precio_registrado=producto.precio,
            stock_registrado=producto.stock,
            accion="TURNO",
            observaciones=f"Fecha del turno: {form.instance.fecha_hora.strftime('%d-%m-%Y %H:%M')}"
        )

        return response


class TurnoEventsView(View):
    def get(self, request, *args, **kwargs):
        cosmetologa_id = request.GET.get('cosmetologa')
        turnos = Turno.objects.select_related('cosmetologa').prefetch_related('tratamientos')

        if cosmetologa_id:
            turnos = turnos.filter(cosmetologa_id=cosmetologa_id)

        eventos = []
        
        for turno in turnos:
            eventos.append({
                "id": turno.id,
                "title": f"{turno.cosmetologa.nombre} - {', '.join([t.descripcion for t in turno.tratamientos.all()])}",
                "start": turno.fecha_hora.isoformat(),
                "url": f"/turnos/editar/{turno.id}"
            })

        return JsonResponse(eventos, safe=False)

# Create your views here.
