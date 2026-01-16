

from datetime import datetime
from django.shortcuts import render

from cosmiatras.models import Cosmetologa
from turnos.models import Turno, TurnoProducto
from productos.models import Producto
from .forms import ReporteCosmiatraForm, ReporteProductoForm


def reporte_cosmiatra(request):
    form = ReporteCosmiatraForm(request.GET or None)

    turnos=""
    total=""
    comision=""
    porcentaje=""
    lista_turnos = []
    
    if form.is_valid():
        fecha_desde = form.cleaned_data.get("fecha_desde")
        fecha_hasta = form.cleaned_data.get("fecha_hasta")
        cosmiatra = form.cleaned_data.get("cosmiatra")
        porcentaje = form.cleaned_data.get("porcentaje")
           
        cosmetologa = Cosmetologa.objects.get(pk=cosmiatra.pk)

        if fecha_desde and fecha_hasta:
            fecha_hasta = datetime.combine(fecha_hasta, datetime.max.time()) 
            fecha_desde = datetime.combine(fecha_desde, datetime.min.time())

            turnos = Turno.objects.filter( 
                fecha_hora__range=(fecha_desde, fecha_hasta), 
                cosmetologa=cosmetologa, pagado=True
            ).order_by("-fecha_hora")

            total = 0            

            for turno in turnos:
                total = total + turno.monto
                productos = TurnoProducto.objects.filter(turno=turno.pk)

                lista_turnos.append(
                    {
                        "fecha": turno.fecha_hora,
                        "monto": turno.monto,
                        "paciente": turno.nombrepaciente.upper(),
                        "producto": " - ".join([p.producto.descripcion for p in productos]),
                        "tratamiento": " - ".join([t.descripcion for t in turno.tratamientos.all()]),
                    }
                ) 

            comision = total * porcentaje / 100

    return render(
        request, 
        "reportes/reporte_cosmiatra.html", 
        {
            "form": form, 
            "turnos": lista_turnos, 
            "total": total,
            "comision": comision,
            "porcentaje": porcentaje
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


# Create your views here.
