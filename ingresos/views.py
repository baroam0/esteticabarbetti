
from datetime import date
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from .models import Ingreso

def ingresos_view(request):

    # -----------------------------
    # 1. Guardar / Editar ingreso
    # -----------------------------
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

    # -----------------------------
    # 2. Filtros por año y mes
    # -----------------------------
    current_year = date.today().year
    last_year = current_year - 1

    anio = request.GET.get("anio", current_year)
    mes = request.GET.get("mes", "0")  # 0 = todos los meses

    ingresos_list = Ingreso.objects.filter(usuario=request.user).order_by("-fecha")

    # Filtrar por año
    if anio:
        ingresos_list = ingresos_list.filter(fecha__year=anio)

    # Filtrar por mes (si mes != 0)
    if mes != "0":
        ingresos_list = ingresos_list.filter(fecha__month=mes)

    # -----------------------------
    # 3. Calcular ingresos, egresos y saldo del período filtrado
    # -----------------------------
    ingreso_dinero = sum(i.monto for i in ingresos_list if i.monto > 0)
    egreso_dinero = sum(i.monto for i in ingresos_list if i.monto < 0)
    saldo = ingreso_dinero + egreso_dinero

    # -----------------------------
    # 4. Paginación
    # -----------------------------
    paginator = Paginator(ingresos_list, 20)
    page_number = request.GET.get("page")
    ingresos = paginator.get_page(page_number)

    # -----------------------------
    # 5. Render
    # -----------------------------
    return render(request, "ingresos/ingresos.html", {
        "ingresos": ingresos,
        "saldo": saldo,
        "ingreso_dinero": ingreso_dinero,
        "egreso_dinero": egreso_dinero,
        "current_year": current_year,
        "last_year": last_year,
        "anio_seleccionado": int(anio),
        "mes_seleccionado": int(mes),
    })



# Create your views here.
