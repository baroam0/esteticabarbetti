
from datetime import datetime
from decimal import Decimal

from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .models import Turno, TurnoProducto
from .forms import TurnoForm, TurnoProductoFormSet

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
                "title": f"{turno.nombrepaciente.upper()}  - {', '.join([t.descripcion for t in turno.tratamientos.all()])}",
                "start": turno.fecha_hora.isoformat(),
                "url": f"/turnos/editar/{turno.id}"
            })

        return JsonResponse(eventos, safe=False)


class TurnoCreateView(CreateView):
    model = Turno
    form_class = TurnoForm
    template_name = 'turnos/turno_form.html'
    success_url = reverse_lazy('turno_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.POST:
            context['formset'] = TurnoProductoFormSet(self.request.POST) 
        else:
            context['formset'] = TurnoProductoFormSet()

        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if not formset.is_valid():
            return self.form_invalid(form) 

        with transaction.atomic():
            
            form.instance.usuario = self.request.user
            self.object = form.save() # self.object ya tiene PK

            formset.instance = self.object
            turno_productos = formset.save(commit=False)
            productos_a_loguear = []

            for tp_instance in turno_productos:
                producto = tp_instance.producto
                cantidad = tp_instance.cantidad_consumida or Decimal(0)
                
                if producto.stock < cantidad:
                    messages.error(self.request, f"Stock insuficiente: {producto.descripcion}. Disponible: {producto.stock}, Requerido: {cantidad}")
                    return self.form_invalid(form) 

                producto.stock -= cantidad
                producto.save()
                
                productos_a_loguear.append(producto)
                tp_instance.save()

            for producto in productos_a_loguear:
                HistorialProducto.objects.create(
                    producto=producto,
                    usuario=self.request.user,
                    precio_registrado=producto.precio,
                    stock_registrado=producto.stock, # Stock DESPUÉS del consumo
                    accion="TURNO",
                    observaciones=f"Consumo fraccionado. Fecha del turno: {self.object.fecha_hora.strftime('%d-%m-%Y %H:%M')}"
                )

        return redirect(self.success_url)


class TurnoUpdateView(UpdateView):
    model = Turno
    form_class = TurnoForm
    template_name = 'turnos/turno_form.html'
    success_url = reverse_lazy('turno_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = TurnoProductoFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = TurnoProductoFormSet(instance=self.object)

        context['productos_seleccionados_en_turno'] = self.object.productos.all()
        
        return context

    def form_valid(self, form):        
        context = self.get_context_data()
        formset = context['formset']
        
        if not formset.is_valid():
            return self.form_invalid(form)
            
        
        with transaction.atomic():
            productos_antes = {}
            for tp in TurnoProducto.objects.filter(turno=self.object):
                productos_antes[tp.producto_id] = tp.cantidad_consumida or Decimal(0)
            
            form.instance.usuario = self.request.user
            self.object = form.save()

            formset.instance = self.object
            new_tp_instances = formset.save(commit=False)

            for tp_instance in formset.deleted_objects:
                producto = tp_instance.producto
                cantidad = tp_instance.cantidad_consumida or Decimal(0)

                producto.stock += cantidad
                producto.save()
                
                HistorialProducto.objects.create(
                    producto=producto,
                    usuario=self.request.user,
                    precio_registrado=producto.precio,
                    stock_registrado=producto.stock,
                    accion="EDITADO", 
                    observaciones=f"Reposición por eliminación de producto en Turno {self.object.id}"
                )

                tp_instance.delete()

            for tp_instance in new_tp_instances:
                producto = tp_instance.producto

                nueva_cantidad = tp_instance.cantidad_consumida or Decimal(0)

                cantidad_anterior = productos_antes.get(producto.id, Decimal(0))
                
                diferencia = nueva_cantidad - cantidad_anterior
                
                if diferencia > Decimal(0):
                    if producto.stock < diferencia:
                        messages.error(self.request, f"Stock insuficiente para ajustar {producto.descripcion}. Disponible: {producto.stock}, Adicional requerido: {diferencia}")
                        return self.form_invalid(form)
                    
                    producto.stock -= diferencia
                    accion_historial = "TURNO" # Consumo
                    
                elif diferencia < Decimal(0):
                    producto.stock += abs(diferencia)
                    accion_historial = "EDITADO"
                else:
                    tp_instance.save()
                    continue

                producto.save()
                tp_instance.save()
                
                HistorialProducto.objects.create(
                    producto=producto,
                    usuario=self.request.user,
                    precio_registrado=producto.precio,
                    stock_registrado=producto.stock,
                    accion=accion_historial, # Usamos la acción definida
                    #observaciones=f"Ajuste por edición de Turno. Diferencia: {diferencia}. Stock final: {producto.stock}"
                    observaciones=f"Ajuste por edición de Turno. Fecha del turno: {self.object.fecha_hora.strftime('%d-%m-%Y %H:%M')}"
                )
                
            return redirect(self.success_url)

# Create your views here.
