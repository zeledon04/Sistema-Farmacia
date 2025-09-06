from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect, render
import os
from django.conf import settings
# Create your views here.
from django.http import JsonResponse
from django.utils import timezone
from farmacia.models import Cajas, Categoria, Categoriaropa, Denominacionescaja, Detallefacturas, Detallefacturasropa, Facturas, Lotes, Opciones, Presentaciones, Productos, Productosropa, Unidadmedidas, Usuarios
from django.contrib import messages
from django.templatetags.static import static
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json

from .utils import admin_required, logout_required, login_required
from django.contrib.auth import logout, authenticate
from django.db.models import F, Sum, ExpressionWrapper, FloatField
from django.core.paginator import Paginator
from datetime import datetime, date, timedelta
from django.utils.timezone import localtime
from django.http import JsonResponse
from django.utils.timezone import now


def notificar_stock_bajo():
    productos_bajos = Productos.objects.filter(stock__lte=30, estado=1)

    notificaciones = []
    
    for producto in productos_bajos:
        notificaciones.append({
            'id': producto.productoid,
            'nombre': producto.nombre,
            'stock': producto.stock
        })
    return notificaciones

def notificar_vencimientos():
    hoy = date.today()
    # 4 meses ≈ 120 días
    limite = hoy + timedelta(days=120)
    proximos_vencimientos = Lotes.objects.filter(fechavencimiento__lte=limite, estado=1)
    
    notificaciones = []
    
    for lote in proximos_vencimientos:
        producto = lote.productoid
        notificaciones.append({
            'id': producto.productoid,
            'nombre': producto.nombre,
            'fecha_vencimiento': lote.fechavencimiento,
            'loteid': lote.loteid
        })
    
    return notificaciones

def datosUser(request):
    user = Usuarios.objects.get(pk=request.session['user_id'])
    notisStock = notificar_stock_bajo()
    notisVencimiento = notificar_vencimientos()
    
    return {
        'user': user,
        'nombre': user.nombre,
        'userId': user.usuarioid,
        'rolid': user.rolid.rolid,
        'notisStock': notisStock,
        'notisVencimiento': notisVencimiento,
        'numeroNotificaciones': len(notisVencimiento) + len(notisStock),
    }
    
@logout_required
def login(request):
    if request.method == 'POST':
        username = request.POST.get('usuario')
        password = request.POST.get('contrasena')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['user_id'] = user.pk
            return redirect('dashboard')
        else:
            return render(request, 'pages/login.html', {'error': 'Credenciales inválidas'})
    else:
        return render(request, 'pages/login.html')
    
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user_data = datosUser(request)
    caja_abierta = Cajas.objects.filter(usuarioid=request.session['user_id'], estado=1).first()

    total_productos = Productos.objects.count() + Productosropa.objects.count()
    
    
    if caja_abierta:
        facturas_caja = Facturas.objects.filter(cajaid=str(caja_abierta.cajaid), estado=1)

        detalles = Detallefacturas.objects.filter(facturaid__in=facturas_caja).values('facturaid').annotate(
            total=Sum(ExpressionWrapper(F('cantidad') * F('precio'), output_field=FloatField()))
        )
        totales_detalles = {d['facturaid']: d['total'] for d in detalles}

        detalles_ropa = Detallefacturasropa.objects.filter(facturaid__in=facturas_caja).values('facturaid').annotate(
            total=Sum(ExpressionWrapper(F('cantidad') * F('precio'), output_field=FloatField()))
        )
        totales_ropa = {d['facturaid']: d['total'] for d in detalles_ropa}

        efectivo_cordobas = caja_abierta.cordobasinicial or 0
        efectivo_dolares = caja_abierta.dolaresinicial or 0

        ingresos_cordobas = 0
        total_ventas = 0
        if facturas_caja:
            
            for factura in facturas_caja:
                cordobas_recibidos = factura.cordobas or 0
                dolares_recibidos = factura.dolares or 0
                tasa = factura.tasacambio or 0

                total_factura = totales_detalles.get(factura.facturaid, 0) + totales_ropa.get(factura.facturaid, 0)
                total_pagado_en_cordobas = cordobas_recibidos + (dolares_recibidos * tasa)
                vuelto = total_pagado_en_cordobas - total_factura

                # Sumamos solo lo que realmente se recibió
                efectivo_cordobas += cordobas_recibidos
                efectivo_dolares += dolares_recibidos

                # Restamos el vuelto en C$
                efectivo_cordobas -= max(vuelto, 0)

                # Ingresos contables (para reportes, no afecta físico)
                ingresos_cordobas += total_factura
                total_ventas = facturas_caja.count()
        else:
            total_ventas = 0

        datos = {
            **user_data,
            'hora': caja_abierta.fechaapertura.strftime('%H:%M:%S'),
            'caja': caja_abierta,
            'efectivo_cordobas': round(efectivo_cordobas, 2),
            'efectivo_dolares': round(efectivo_dolares, 2),
            'ingresos_cordobas': round(ingresos_cordobas, 2),
            'ingresos_dolares': 0,
            'total_productos': total_productos,
            'total_ventas': total_ventas,
        }

        return render(request, 'pages/home.html', datos)

    return render(request, 'pages/home.html', {**user_data, 'total_productos': total_productos})

@admin_required
def opciones(request):
    user_data = datosUser(request)
    opc = Opciones.objects.first()
    datos = {**user_data, 'opcion': opc}
    if request.method == 'POST':
        tasa = request.POST.get('tasa')
        if tasa:
            try:
                tasa = float(tasa)
                if tasa <= 0:
                    messages.error(request, "La tasa Invalida.")
                else:
                    opc.tasacambio = tasa
                    opc.save()
                    messages.success(request, "Tasa de cambio actualizada correctamente.")
            except ValueError:
                messages.error(request, "Por favor, ingresa un valor numérico válido para la tasa de cambio.")

        
    return render(request, 'pages/opciones.html', datos)

def obtener_tasa_cambio(request):
    try:
        opcion = Opciones.objects.first()
        tasa = opcion.tasacambio if opcion else None
        return JsonResponse({'tasaCambio': tasa})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)