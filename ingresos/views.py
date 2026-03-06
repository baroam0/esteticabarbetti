
from datetime import datetime, time
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from .models import Ingreso


def ingresos_view(request):
    hoy = timezone.localdate()

    inicio_hoy = timezone.make_aware(datetime.combine(hoy, time.min))
    fin_hoy = timezone.make_aware(datetime.combine(hoy, time.max))

    ingresoshoy = Ingreso.objects.filter(
        usuario=request.user,
        fecha__range=(inicio_hoy, fin_hoy)
    ).order_by("-fecha")

    if ingresoshoy:
        ingreso_dinero_hoy = sum(i.monto for i in ingresoshoy if i.monto > 0)
        egreso_dinero_hoy = sum(i.monto for i in ingresoshoy if i.monto < 0)
        saldo_hoy = ingreso_dinero_hoy + egreso_dinero_hoy
    else:
        ingreso_dinero_hoy = 0
        egreso_dinero_hoy = 0
        saldo_hoy = 0


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

    fecha_desde = request.GET.get("fecha_desde", "")
    fecha_hasta = request.GET.get("fecha_hasta", "")
    turnofiltro = request.GET.get("turnofiltro", "A")

    ingresos_list = Ingreso.objects.filter(usuario=request.user).order_by("-id")

    if fecha_desde:
        fecha_desde_dt = datetime.combine(
            datetime.strptime(fecha_desde, "%Y-%m-%d").date(),
            time.min
        )
        ingresos_list = ingresos_list.filter(fecha__gte=fecha_desde_dt)

    if fecha_hasta:
        fecha_hasta_dt = datetime.combine(
            datetime.strptime(fecha_hasta, "%Y-%m-%d").date(),
            time.max
        )
        ingresos_list = ingresos_list.filter(fecha__lte=fecha_hasta_dt)

    if turnofiltro == "M":
        limite = time(13, 30)
        ingresos_list = ingresos_list.filter(
            fecha__time__gte=time(6,0), fecha__time__lt=limite
        )

    elif turnofiltro == "T":
        limite = time(13, 30) # 13:30 
        ingresos_list = ingresos_list.filter(
            fecha__time__gte=limite, fecha__time__lt=time(23, 0)
        )
    
    if ingresos_list:
        ingreso_dinero = sum(i.monto for i in ingresos_list if i.monto > 0)
        egreso_dinero = sum(i.monto for i in ingresos_list if i.monto < 0)
        saldo = ingreso_dinero + egreso_dinero
    else:
        ingreso_dinero = 0
        egreso_dinero = 0
        saldo = ingreso_dinero + egreso_dinero

    paginator = Paginator(ingresos_list, 20)
    page_number = request.GET.get("page")
    ingresos = paginator.get_page(page_number)

    return render(request, "ingresos/ingresos.html", {
        "ingresos": ingresos,
        "saldo": saldo,
        "ingreso_dinero": ingreso_dinero,
        "egreso_dinero": egreso_dinero,
        "ingresoshoy": ingresoshoy,
        "fecha_desde": fecha_desde,
        "fecha_hasta": fecha_hasta,
        "turno": turnofiltro,
        "ingreso_dinero_hoy": ingreso_dinero_hoy,
        "egreso_dinero_hoy": egreso_dinero_hoy,
        "saldo_hoy": saldo_hoy
    })


def ingresos_view2(request):
    hoy = timezone.localdate()

    inicio_hoy = timezone.make_aware(datetime.combine(hoy, time.min))
    fin_hoy = timezone.make_aware(datetime.combine(hoy, time.max))

    ingresoshoy = Ingreso.objects.filter(
        usuario=request.user,
        fecha__range=(inicio_hoy, fin_hoy)
    ).order_by("-fecha")

    if ingresoshoy:
        ingreso_dinero_hoy = sum(i.monto for i in ingresoshoy if i.monto > 0)
        egreso_dinero_hoy = sum(i.monto for i in ingresoshoy if i.monto < 0)
        saldo_hoy = ingreso_dinero_hoy + egreso_dinero_hoy
    else:
        ingreso_dinero_hoy = 0
        egreso_dinero_hoy = 0
        saldo_hoy = 0


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

    fecha_desde = request.GET.get("fecha_desde", "")
    fecha_hasta = request.GET.get("fecha_hasta", "")
    turnofiltro = request.GET.get("turnofiltro", "A")

    ingresos_list = Ingreso.objects.filter(usuario=request.user).order_by("-id")

    if fecha_desde:
        fecha_desde_dt = datetime.combine(
            datetime.strptime(fecha_desde, "%Y-%m-%d").date(),
            time.min
        )
        ingresos_list = ingresos_list.filter(fecha__gte=fecha_desde_dt)

    if fecha_hasta:
        fecha_hasta_dt = datetime.combine(
            datetime.strptime(fecha_hasta, "%Y-%m-%d").date(),
            time.max
        )
        ingresos_list = ingresos_list.filter(fecha__lte=fecha_hasta_dt)

    if turnofiltro == "M":
        limite = time(13, 30)
        ingresos_list = ingresos_list.filter(
            fecha__time__gte=time(6,0), fecha__time__lt=limite
        )

    elif turnofiltro == "T":
        limite = time(13, 30) # 13:30 
        ingresos_list = ingresos_list.filter(
            fecha__time__gte=limite, fecha__time__lt=time(23, 0)
        )
    
    if ingresos_list:
        ingreso_dinero = sum(i.monto for i in ingresos_list if i.monto > 0)
        egreso_dinero = sum(i.monto for i in ingresos_list if i.monto < 0)
        saldo = ingreso_dinero + egreso_dinero
    else:
        ingreso_dinero = 0
        egreso_dinero = 0
        saldo = ingreso_dinero + egreso_dinero

    paginator = Paginator(ingresos_list, 20)
    page_number = request.GET.get("page")
    ingresos = paginator.get_page(page_number)

    return render(request, "ingresos/ingresos2.html", {
        "ingresos": ingresos,
        "saldo": saldo,
        "ingreso_dinero": ingreso_dinero,
        "egreso_dinero": egreso_dinero,
        "ingresoshoy": ingresoshoy,
        "fecha_desde": fecha_desde,
        "fecha_hasta": fecha_hasta,
        "turno": turnofiltro,
        "ingreso_dinero_hoy": ingreso_dinero_hoy,
        "egreso_dinero_hoy": egreso_dinero_hoy,
        "saldo_hoy": saldo_hoy
    })


def ingresos_view3(request):
    hoy = timezone.localdate()

    inicio_hoy = timezone.make_aware(datetime.combine(hoy, time.min))
    fin_hoy = timezone.make_aware(datetime.combine(hoy, time.max))

    ingresoshoy = Ingreso.objects.filter(
        usuario=request.user,
        fecha__range=(inicio_hoy, fin_hoy)
    ).order_by("-fecha")

    tmpingresoshoylist = list()
    tmpingresoshoydict = dict()

    for i in ingresoshoy:
        if i.monto > 0:
            tmpingresoshoydict = {
                "id": i.id,
                "fecha": i.fecha,
                "descripcion": i.descripcion,
                "monto": i.monto,
                "esingreso": True,
            }
            tmpingresoshoylist.append(tmpingresoshoydict)
            tmpingresoshoydict = dict()
        else:
            tmpingresoshoydict = {
                "id": i.id,
                "descripcion": i.descripcion,
                "monto": i.monto,
                "esingreso": False,
            }
            tmpingresoshoylist.append(tmpingresoshoydict)
            tmpingresoshoydict = dict()
    
    tmpingresoshoylist = sorted(tmpingresoshoylist, key=lambda x: x["esingreso"], reverse=True)

    if ingresoshoy:
        ingreso_dinero_hoy = sum(i.monto for i in ingresoshoy if i.monto > 0)
        egreso_dinero_hoy = sum(i.monto for i in ingresoshoy if i.monto < 0)
        saldo_hoy = ingreso_dinero_hoy + egreso_dinero_hoy
    else:
        ingreso_dinero_hoy = 0
        egreso_dinero_hoy = 0
        saldo_hoy = 0


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
        return redirect("ingresos3")

    fecha_desde = request.GET.get("fecha_desde", "")
    fecha_hasta = request.GET.get("fecha_hasta", "")
    turnofiltro = request.GET.get("turnofiltro", "A")

    ingresos_list = Ingreso.objects.filter(usuario=request.user).order_by("-id")

    if fecha_desde:
        fecha_desde_dt = datetime.combine(
            datetime.strptime(fecha_desde, "%Y-%m-%d").date(),
            time.min
        )
        ingresos_list = ingresos_list.filter(fecha__gte=fecha_desde_dt)

    if fecha_hasta:
        fecha_hasta_dt = datetime.combine(
            datetime.strptime(fecha_hasta, "%Y-%m-%d").date(),
            time.max
        )
        ingresos_list = ingresos_list.filter(fecha__lte=fecha_hasta_dt)

    if turnofiltro == "M":
        limite = time(13, 30)
        ingresos_list = ingresos_list.filter(
            fecha__time__gte=time(6,0), fecha__time__lt=limite
        )

    elif turnofiltro == "T":
        limite = time(13, 30) # 13:30 
        ingresos_list = ingresos_list.filter(
            fecha__time__gte=limite, fecha__time__lt=time(23, 0)
        )
    
    if ingresos_list:
        ingreso_dinero = sum(i.monto for i in ingresos_list if i.monto > 0)
        egreso_dinero = sum(i.monto for i in ingresos_list if i.monto < 0)
        saldo = ingreso_dinero + egreso_dinero
    else:
        ingreso_dinero = 0
        egreso_dinero = 0
        saldo = ingreso_dinero + egreso_dinero

    paginator = Paginator(ingresos_list, 20)
    page_number = request.GET.get("page")
    ingresos = paginator.get_page(page_number)

    return render(request, "ingresos/ingresos3.html", {
        "ingresos": ingresos,
        "saldo": saldo,
        "ingreso_dinero": ingreso_dinero,
        "egreso_dinero": egreso_dinero,
        "ingresoshoy": ingresoshoy,
        "tmpingresoshoylist": tmpingresoshoylist,
        "fecha_desde": fecha_desde,
        "fecha_hasta": fecha_hasta,
        "turno": turnofiltro,
        "ingreso_dinero_hoy": ingreso_dinero_hoy,
        "egreso_dinero_hoy": egreso_dinero_hoy,
        "saldo_hoy": saldo_hoy
    })
