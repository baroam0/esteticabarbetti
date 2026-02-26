from datetime import datetime, time, timedelta

from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone


from cosmiatras.models import Cosmetologa
from turnos.models import Turno, TurnoProducto
from productos.models import Producto
from .forms import ReporteCosmiatraForm, ReporteProductoForm

def reporte_cosmiatra(request):
    form = ReporteCosmiatraForm(request.GET or None)

    botonescosmiatras = Cosmetologa.objects.all().order_by("apellido")

    lista_turnos = []
    total = 0
    comision = 0
    porcentaje = ""

    if form.is_valid():
        fecha_desde = form.cleaned_data["fecha_desde"]
        fecha_hasta = form.cleaned_data["fecha_hasta"]
        cosmiatra = form.cleaned_data["cosmiatra"]   # instancia o None
        porcentaje = form.cleaned_data["porcentaje"]
        turno = form.cleaned_data["turno"]

        # Rango horario
        if turno == "manana":
            fecha_desde = datetime.combine(fecha_desde, time(6, 0))
            fecha_hasta = datetime.combine(fecha_hasta, time(13, 0))
        elif turno == "tarde":
            fecha_desde = datetime.combine(fecha_desde, time(13, 0))
            fecha_hasta = datetime.combine(fecha_hasta, time(22, 0))
        else:
            fecha_desde = datetime.combine(fecha_desde, datetime.min.time())
            fecha_hasta = datetime.combine(fecha_hasta, datetime.max.time())

        # Query base: TODOS los turnos pagados en rango
        turnos = Turno.objects.filter(
            fecha_hora__range=(fecha_desde, fecha_hasta),
            pagado=True
        )

        # Si eligió una cosmiatra específica, filtramos
        if cosmiatra is not None:
            turnos = turnos.filter(cosmetologa=cosmiatra)

        turnos = turnos.order_by("-fecha_hora")

        # Procesar turnos
        for turno in turnos:
            total += turno.monto
            productos = TurnoProducto.objects.filter(turno=turno.pk)

            lista_turnos.append({
                "fecha": turno.fecha_hora,
                "monto": turno.monto,
                "paciente": turno.nombrepaciente.upper(),
                "cosmiatra": turno.cosmetologa,
                "producto": " - ".join([p.producto.descripcion for p in productos]),
                "tratamiento": " - ".join([t.descripcion for t in turno.tratamientos.all()]),
                "observaciones": turno.observaciones
            })

        comision = total * porcentaje / 100
    
    return render(
        request, 
        "reportes/reporte_cosmiatra.html", 
        {
            "form": form, 
            "turnos": lista_turnos, 
            "total": total,
            "comision": comision,
            "porcentaje": porcentaje,
            "botonescosmiatras": botonescosmiatras
        }
    )


def reporte_productos(request):
    form = ReporteProductoForm(request.GET or None)

    lista_productos = []
    total = 0

    if form.is_valid():
        fecha_desde = form.cleaned_data.get("fecha_desde")
        fecha_hasta = form.cleaned_data.get("fecha_hasta")
        cosmiatra = form.cleaned_data.get("cosmiatra")
        producto = form.cleaned_data.get("producto")

        if cosmiatra:
            cosmetologas = Cosmetologa.objects.filter(pk=cosmiatra.pk)
        else:
            cosmetologas = Cosmetologa.objects.all()

        if producto:
            productos = Producto.objects.filter(pk=producto.pk)
        else:
            productos = Producto.objects.all()

        if fecha_desde and fecha_hasta:
            fecha_desde = datetime.combine(fecha_desde, datetime.min.time())
            fecha_hasta = datetime.combine(fecha_hasta, datetime.max.time())

            turnos = Turno.objects.filter(
                fecha_hora__range=(fecha_desde, fecha_hasta),
                cosmetologa__in=cosmetologas,
                pagado=True
            )

            turnosproductos = TurnoProducto.objects.filter(
                turno__in=turnos,
                producto__in=productos
            ).select_related("turno", "producto", "turno__cosmetologa")

            for tp in turnosproductos:
                gasto = round(tp.cantidad_consumida * tp.producto.precio, 2)

                lista_productos.append({
                    "fecha": tp.turno.fecha_hora,
                    "cosmiatra": tp.turno.cosmetologa,
                    "producto": tp.producto.descripcion.upper(),
                    "cantidad": tp.cantidad_consumida,
                    "monto_fraccionado": gasto,
                    "monto": tp.producto.precio,
                })

                total += gasto

    return render(
        request,
        "reportes/reporte_producto.html",
        {
            "form": form,
            "productos": lista_productos,
            "total": total
        }
    )



def grafico_tratamientos(request):
    fecha_desde_str = request.GET.get("fecha_desde")
    fecha_hasta_str = request.GET.get("fecha_hasta")

    labels = []
    valores = []

    if fecha_desde_str and fecha_hasta_str:
        fecha_desde = datetime.strptime(fecha_desde_str, "%Y-%m-%d").date()
        fecha_hasta = datetime.strptime(fecha_hasta_str, "%Y-%m-%d").date()

        inicio = datetime.combine(fecha_desde, datetime.min.time())
        fin = datetime.combine(fecha_hasta, datetime.max.time())

        datos = (
            Turno.objects.filter(fecha_hora__range=(inicio, fin))
            .values("tratamientos__descripcion")
            .annotate(total=Count("tratamientos"))
            .order_by("-total")
        )

        labels = [item["tratamientos__descripcion"] for item in datos]
        valores = [item["total"] for item in datos]    

    contexto = {
        "fecha_desde_str": fecha_desde_str,
        "fecha_hasta_str": fecha_hasta_str,
        "labels": labels,
        "valores": valores,
    }

    return render(request, "reportes/grafico_tratamientos.html", contexto)



def ajax_turno_cosmiatra(request):
    cosmiatra_id = request.GET.get("cosmiatra_id")
    cosmetologa = Cosmetologa.objects.get(pk=cosmiatra_id)
    turno = request.GET.get("turno")

    hoy = timezone.localdate()

    if turno == "manana":
        fecha_desde = timezone.make_aware(datetime.combine(hoy, time(6, 0)))
        fecha_hasta = timezone.make_aware(datetime.combine(hoy, time(13, 0)))
    elif turno == "tarde":
        fecha_desde = timezone.make_aware(datetime.combine(hoy, time(13, 0)))
        fecha_hasta = timezone.make_aware(datetime.combine(hoy, time(22, 0)))
    else:
        fecha_desde = timezone.make_aware(datetime.combine(hoy, time.min))
        fecha_hasta = timezone.make_aware(datetime.combine(hoy, time.max))
    
    turnos = Turno.objects.filter(
        cosmetologa=cosmetologa,
        fecha_hora__range=(fecha_desde, fecha_hasta),
        pagado=True
    ).order_by("-fecha_hora")

    total = 0
    comision = 0

    if turnos:
        for turno in turnos:
            total = total + turno.monto
    
    comision = total * 20 / 100

    data = []
    for t in turnos:
        data.append({
            "fecha": timezone.localtime(t.fecha_hora).strftime("%d/%m/%Y %H:%M"),        
            "paciente": t.nombrepaciente.upper() if t.nombrepaciente else "-",
            "tratamientos": " - ".join([tr.descripcion for tr in t.tratamientos.all()]),
            "productos": " - ".join([p.descripcion for p in t.productos.all()]),
            "monto": str(t.monto),
            "modo_pago": t.get_modo_pago_display(),
            "observaciones": t.observaciones or "-",
            "comision": comision,
        })

    total = sum(t.monto for t in turnos if t.monto)

    return JsonResponse({"turnos": data, "total": str(total), "comision": str(comision)})

# Create your views here.
