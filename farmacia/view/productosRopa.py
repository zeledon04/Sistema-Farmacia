
from django.shortcuts import get_object_or_404, redirect, render
import os
from django.conf import settings
# Create your views here.
from django.http import JsonResponse
from django.utils import timezone
from farmacia.models import  Categoriaropa, Detallefacturasropa, Productosropa
from django.contrib import messages

from django.utils import timezone


from farmacia.views import datosUser

from ..utils import admin_required, login_required
from django.core.paginator import Paginator
from django.http import JsonResponse



# Productos Ropa---------------------------------------
@login_required
def listarProductoRopa(request):
    categorias = Categoriaropa.objects.filter(estado=1)
    
    productosRopa_queryset = Productosropa.objects.filter(estado=1).select_related('categoriaropaid').order_by('-productoropaid')
    paginator = Paginator(productosRopa_queryset, 50)
    
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    cont = (page_obj.number - 1) * paginator.per_page + 1
    for producto in page_obj:
        producto.cont = cont
        cont += 1
    
    user_data = datosUser(request)
    
    return render(request, 'pages/productosRopa/listarProductosRopa.html', {
        **user_data,
        'productosRopa': page_obj,
        'categorias' : categorias
        })

@admin_required
def agregarProductoRopa(request):
    categoriasRopa = Categoriaropa.objects.filter(estado = 1)
    user_data = datosUser(request)
    datos = {**user_data, 'categoriasRopa' : categoriasRopa}
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        codigobarra = request.POST.get('codigoBarraRopa')
        descripcion = request.POST.get('descripcion')
        categoriaRopaId = request.POST.get('categoriaropaid')
        talla = request.POST.get('talla')
        precio = request.POST.get('precio')
        ruta = nombre.replace(" ", "") + codigobarra + '.jpg'
            
        ruta = 'defaultImage.png'

        if 'rutaFoto' in request.FILES:
            file = request.FILES['rutaFoto']
            ruta = nombre.replace(" ", "") + codigobarra + '.jpg'
            path = os.path.join(settings.BASE_DIR, 'farmacia/static/productos/', ruta)

            with open(path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
                    
        productoRopa = Productosropa(
            nombre = nombre,
            codigobarraropa = codigobarra,
            descripcion = descripcion,
            categoriaropaid_id = categoriaRopaId,
            talla = talla,
            precio=precio,
            estado=1,
            rutafoto=ruta,
            updated_at = timezone.now()
        )
        productoRopa.save()
        return redirect('listar_ropa')
    return render(request, 'pages/productosRopa/agregarProductoRopa.html', datos)

@login_required
def filtrar_productos_ropa(request):
    nombre = request.GET.get('nombre', '')
    categoria = request.GET.get('categoria', '')
    talla = request.GET.get('talla', '')
    
    productos = Productosropa.objects.filter(estado=1).order_by('-productoropaid')
    
    if nombre:
        productos = productos.filter(nombre__istartswith=nombre)
    if categoria:
        productos = productos.filter(categoriaropaid=categoria)
    if talla:
        productos = productos.filter(talla=talla)

    data = []
    for i, p in enumerate(productos, 1):
        data.append({
            'cont': i,
            'id': p.productoropaid,
            'nombre': p.nombre,
            'rutafoto': p.rutafoto,
            'categoria': p.categoriaropaid.nombre,
            'talla': p.talla,
            'precio': p.precio,
            'updated_at': int(p.updated_at.timestamp())
        })

    return JsonResponse(data, safe=False)

@admin_required
def actualizarProductoRopa(request, id):
    categoriasRopa = Categoriaropa.objects.filter(estado = 1)
    productoRopa = Productosropa.objects.get(pk=id)
    user_data = datosUser(request)
    datos = {**user_data, 'productoRopa' : productoRopa, 'categoriasRopa' : categoriasRopa}
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        codigobarraRopa = request.POST.get('codigoBarraRopa')
        descripcion = request.POST.get('descripcion')
        categoriaRopaId = request.POST.get('categoriaRopaId')
        talla = request.POST.get('talla')
        precio = request.POST.get('precio')

        nueva_ruta = nombre.replace(" ", "") + codigobarraRopa + '.jpg'
        ruta_anterior = productoRopa.rutafoto
        ruta_archivo_anterior = os.path.join(settings.BASE_DIR, 'farmacia/static/productos/', ruta_anterior)
        nueva_ruta_absoluta = os.path.join(settings.BASE_DIR, 'farmacia/static/productos/', nueva_ruta)

        if 'rutaFoto' in request.FILES:
            file = request.FILES['rutaFoto']

            with open(nueva_ruta_absoluta, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            if ruta_anterior != nueva_ruta and os.path.exists(ruta_archivo_anterior) and ruta_anterior != 'defaultImage.png':
                os.remove(ruta_archivo_anterior)
            productoRopa.rutafoto = nueva_ruta

        elif nombre.replace(" ", "") + codigobarraRopa + '.jpg' != ruta_anterior:
            if os.path.exists(ruta_archivo_anterior):
                os.rename(ruta_archivo_anterior, nueva_ruta_absoluta)
            productoRopa.rutafoto = nueva_ruta

        productoRopa.nombre = nombre
        productoRopa.codigobarraropa = codigobarraRopa
        productoRopa.descripcion = descripcion
        productoRopa.categoriaropaid_id = categoriaRopaId
        productoRopa.talla = talla
        productoRopa.precio = precio
        productoRopa.updated_at = timezone.now()

        productoRopa.save()

        messages.success(request, "¡Producto Ropa actualizado correctamente!")
        return redirect('listar_ropa')
    return render(request, 'pages/productosRopa/actualizarProductoRopa.html', datos)

@admin_required
def eliminarProductoRopa(request, id):
    productoRopa = get_object_or_404(Productosropa, pk=id)
    productoRopa.estado = 0
    productoRopa.save()
    messages.success(request, "Producto Ropa " + productoRopa.nombre + " Eliminado Correctamente.")
    return redirect('listar_ropa')

@login_required
def historialVentasRopa(request):
    ventas_queryset = Detallefacturasropa.objects.filter(estado=1).order_by('-detallefacturaropaid')
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
    return render(request, 'pages/productosRopa/historialVentasRopa.html', datos)
