
from django.shortcuts import get_object_or_404, redirect, render
import os
from django.conf import settings
# Create your views here.
from django.http import JsonResponse
from django.utils import timezone
from farmacia.models import Categoria, Detallefacturas, Detallefacturasropa, Lotes, Presentaciones, Productos, Unidadmedidas, Usuarios
from django.contrib import messages
from django.utils import timezone

from farmacia.views import datosUser

from ..utils import admin_required, login_required
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from django.http import JsonResponse


# Productosss---------------------------------------
@login_required
def listarProducto(request):
    user_data = datosUser(request)
    categorias = Categoria.objects.filter(estado=1)
    presentaciones = Presentaciones.objects.filter(estado=1)
    
    productos_queryset = Productos.objects.filter(estado=1).select_related('categoriaid', 'presentacionid').order_by('-productoid')
    
    paginator = Paginator(productos_queryset, 50)  
     
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    cont = (page_obj.number - 1) * paginator.per_page + 1
    for producto in page_obj:
        producto.cont = cont
        cont += 1
    
    return render(request, 'pages/productos/listarProductos.html', {
        **user_data,
        'productos': page_obj, 
        'categorias': categorias, 
        'presentaciones': presentaciones})

@login_required 
def filtrar_productos(request):
    nombre = request.GET.get('nombre', '')
    categoria = request.GET.get('categoria', '')
    presentacion = request.GET.get('presentacion', '')

    productos = Productos.objects.filter(estado=1).order_by('-productoid')

    if nombre:
        productos = productos.filter(nombre__istartswith=nombre)
    if categoria:
        productos = productos.filter(categoriaid_id=categoria)
    if presentacion:
        productos = productos.filter(presentacionid_id=presentacion)

    data = []
    for i, p in enumerate(productos, 1):
        data.append({
            'cont': i,
            'productoid': p.productoid,
            'nombre': p.nombre,
            'rutafoto': p.rutafoto,
            'categoria': p.categoriaid.nombre,
            'presentacion': p.presentacionid.nombre,
            'stock': p.stock,
            'preciounidad': str(p.preciounidad),
            'updated_at': int(p.updated_at.timestamp())  # para refrescar la imagen
        })

    return JsonResponse(data, safe=False)

@admin_required
def agregarProducto(request):
    categorias = Categoria.objects.filter(estado = 1)
    presentaciones = Presentaciones.objects.filter(estado = 1)
    unidadMedida = Unidadmedidas.objects.filter(estado = 1)
    
    user_data = datosUser(request)
    
    datos = {**user_data, 'categorias' : categorias, 'presentaciones' : presentaciones, 'unidadMedida' : unidadMedida}
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        codigobarra = request.POST.get('codigoBarra')
        descripcion = request.POST.get('descripcion')
        categoriaid = request.POST.get('categoriaid')
        presentacionid = request.POST.get('presentacionid')
        concentracion = request.POST.get('concentracion')
        unidadmedidaid = request.POST.get('unidadmedidaid')
        preciounidad = 0
        ruta = nombre.replace(" ", "") + codigobarra + '.jpg'
        
        ruta = 'defaultImage.png'

        if 'rutaFoto' in request.FILES:
            file = request.FILES['rutaFoto']
            ruta = nombre.replace(" ", "") + codigobarra + '.jpg'
            path = os.path.join(settings.BASE_DIR, 'farmacia/static/productos/', ruta)

            with open(path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

        try:
            producto = Productos(
                nombre=nombre,
                codigobarra=codigobarra,
                descripcion=descripcion,
                categoriaid_id=categoriaid,
                presentacionid_id=presentacionid,
                concentracion=concentracion,
                unidadmedidaid_id=unidadmedidaid,
                preciounidad=preciounidad,
                stock=0,
                estado=1,
                rutafoto=ruta,
                updated_at = timezone.now()
            )
            producto.save()
            messages.success(request, "¡Producto actualizado correctamente!")
            return redirect('listar_producto')
            
        except Exception as e:
            if codigobarra and Productos.objects.filter(codigobarra=codigobarra).exists():
                messages.error(request, "El código de barras ya está registrado.")
            else:
                messages.error(request, "Error al agregar el producto: " + str(e))
            return redirect('agregar_producto')
        
    return render(request, 'pages/productos/agregarProducto.html', datos)

@admin_required
def actualizarProducto(request, id):
    categorias = Categoria.objects.filter(estado = 1)
    presentaciones = Presentaciones.objects.filter(estado = 1)
    unidadMedida = Unidadmedidas.objects.filter(estado = 1)
    producto = Productos.objects.get(pk=id)
    
    user_data = datosUser(request)
    datos = {**user_data, 'producto' : producto, 'categorias' : categorias, 'presentaciones' : presentaciones, 'unidadMedida' : unidadMedida}
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        codigobarra = request.POST.get('codigoBarra')
        descripcion = request.POST.get('descripcion')
        categoriaid = request.POST.get('categoriaid')
        presentacionid = request.POST.get('presentacionid')
        concentracion = request.POST.get('concentracion')
        unidadmedidaid = request.POST.get('unidadmedidaid')

        nueva_ruta = nombre.replace(" ", "") + codigobarra + '.jpg'
        ruta_anterior = producto.rutafoto
        ruta_archivo_anterior = os.path.join(settings.BASE_DIR, 'farmacia/static/productos/', ruta_anterior)
        nueva_ruta_absoluta = os.path.join(settings.BASE_DIR, 'farmacia/static/productos/', nueva_ruta)

        # 1. Verifica si se subió nueva imagen
        if 'rutaFoto' in request.FILES:
            file = request.FILES['rutaFoto']
            # Guarda la nueva imagen
            with open(nueva_ruta_absoluta, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            # Borra imagen anterior si es diferente
            
            if ruta_anterior != nueva_ruta and os.path.exists(ruta_archivo_anterior) and ruta_anterior != 'defaultImage.png':
                os.remove(ruta_archivo_anterior)
            producto.rutafoto = nueva_ruta

        # 2. Si no hay nueva imagen pero cambió el nombre, renombrar imagen
        elif nombre.replace(" ", "") + codigobarra + '.jpg' != ruta_anterior:
            if os.path.exists(ruta_archivo_anterior):
                os.rename(ruta_archivo_anterior, nueva_ruta_absoluta)
            producto.rutafoto = nueva_ruta

        # Actualizar los demás campos
        producto.nombre = nombre
        producto.codigobarra = codigobarra
        producto.descripcion = descripcion
        producto.categoriaid_id = categoriaid
        producto.presentacionid_id = presentacionid
        producto.concentracion = concentracion
        producto.unidadmedidaid_id = unidadmedidaid
        producto.updated_at = timezone.now()

        producto.save()

        messages.success(request, "¡Producto actualizado correctamente!")
        return redirect('listar_producto')
    return render(request, 'pages/productos/actualizarProducto.html', datos)

@admin_required
def eliminarProducto(request, id):
    producto = get_object_or_404(Productos, pk=id)
    producto.estado = 0
    producto.save()
    messages.success(request, "Producto " + producto.nombre + " Eliminado Correctamente.")
    return redirect('listar_producto')

@login_required
def historialVentas(request):
    ventas_queryset = Detallefacturas.objects.filter(estado=1).order_by('-detallefacturaid')
    paginator = Paginator(ventas_queryset, 50)
    
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    cont = (page_obj.number - 1) * paginator.per_page + 1
    for producto in page_obj:
        producto.total = producto.cantidad * producto.precio
        producto.cont = cont
        cont += 1
        
    user_data = datosUser(request)
    datos = {**user_data, 'ventas': page_obj}
    return render(request, 'pages/productos/historialVentas.html', datos)


@login_required
def filtrar_ventas(request):
    nombre = request.GET.get("nombre", "")
    fecha_filtro = request.GET.get("fecha", "")
    fecha_inicio = request.GET.get("inicio", "")
    fecha_fin = request.GET.get("fin", "")
    tipo = request.GET.get("tipo")
    
    if tipo == 'farmacia':
        ventas_queryset = Detallefacturas.objects.filter(estado=1)
        if nombre:
            ventas_queryset = ventas_queryset.filter(productoid__nombre__istartswith=nombre)
            
    if tipo == 'tienda':
        ventas_queryset = Detallefacturasropa.objects.filter(estado=1)
        if nombre:
            ventas_queryset = ventas_queryset.filter(productoropaid__nombre__istartswith=nombre)

    if fecha_filtro == "hoy":
        hoy = datetime.now().date()
        ventas_queryset = ventas_queryset.filter(facturaid__fecha__date=hoy)
    elif fecha_filtro == "semana":
        hoy = datetime.today().date()
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        fin_semana = inicio_semana + timedelta(days=6)
        ventas_queryset = ventas_queryset.filter(facturaid__fecha__date__range=[inicio_semana, fin_semana])
    elif fecha_filtro == "mes":
        ahora = datetime.now()
        ventas_queryset = ventas_queryset.filter(facturaid__fecha__year=ahora.year, facturaid__fecha__month=ahora.month)
    elif fecha_filtro == "anio":
        ahora = datetime.now()
        ventas_queryset = ventas_queryset.filter(facturaid__fecha__year=ahora.year)
    elif fecha_filtro == "rango" and fecha_inicio and fecha_fin:
        ventas_queryset = ventas_queryset.filter(facturaid__fecha__date__range=[fecha_inicio, fecha_fin])

    data = []
    cont = 1
    if tipo == 'farmacia':
        for venta in ventas_queryset.order_by('-detallefacturaid'):
            data.append({
                'cont': cont,
                'producto': venta.productoid.nombre,
                'fecha': venta.facturaid.fecha.strftime("%d/%m/%Y %I:%M %p") if venta.facturaid.fecha else '',
                'cantidad': venta.cantidad,
                'precio': venta.precio,
                'precioCompra': venta.preciocompra
            })
            cont += 1
    if tipo == 'tienda':
        for venta in ventas_queryset.order_by('-detallefacturaropaid'):
            data.append({
                'cont': cont,
                'producto': venta.productoropaid.nombre,
                'fecha': venta.facturaid.fecha.strftime("%d/%m/%Y %I:%M %p") if venta.facturaid.fecha else '',
                'cantidad': venta.cantidad,
                'precio': venta.precio,
                'precioCompra': venta.preciocompra
            })
            cont += 1
    return JsonResponse({'ventas': data})
   