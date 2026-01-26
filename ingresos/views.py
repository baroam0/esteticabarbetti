
from datetime import date
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from .models import Ingreso


def ingresos_view(request):
    if request.method == "POST":
        id_ingreso = request.POST.get("id_ingreso")

        if id_ingreso:
            ingreso = get_object_or_404(Ingreso, id=id_ingreso)
        else:
            ingreso = Ingreso()

        ingreso.fecha = request.POST.get("fecha")
        ingreso.descripcion = request.POST.get("descripcion")
        ingreso.monto = request.POST.get("monto")
        ingreso.usuario = request.user
        ingreso.save()

        return redirect("ingresos")

    # --- NUEVOS FILTROS ---
    fecha_desde = request.GET.get("fecha_desde", "")
    fecha_hasta = request.GET.get("fecha_hasta", "")

    ingresos_list = Ingreso.objects.filter(usuario=request.user).order_by("-id")

    if fecha_desde:
        ingresos_list = ingresos_list.filter(fecha__gte=fecha_desde)

    if fecha_hasta:
        ingresos_list = ingresos_list.filter(fecha__lte=fecha_hasta)

    ingreso_dinero = sum(i.monto for i in ingresos_list if i.monto > 0)
    egreso_dinero = sum(i.monto for i in ingresos_list if i.monto < 0)
    saldo = ingreso_dinero + egreso_dinero

    paginator = Paginator(ingresos_list, 20)
    page_number = request.GET.get("page")
    ingresos = paginator.get_page(page_number)

    return render(request, "ingresos/ingresos.html", {
        "ingresos": ingresos,
        "saldo": saldo,
        "ingreso_dinero": ingreso_dinero,
        "egreso_dinero": egreso_dinero,
        "fecha_desde": fecha_desde,
        "fecha_hasta": fecha_hasta,
    })

# Create your views here.
