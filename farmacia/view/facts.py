
from django.shortcuts import redirect, render
# Create your views here.
from django.http import JsonResponse
from django.utils import timezone
from farmacia.models import Cajas, Detallefacturas, Detallefacturasropa, Facturas, Lotes, Opciones, Productos, Productosropa, Usuarios
from django.contrib import messages
from django.templatetags.static import static
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json

from farmacia.views import datosUser

from ..utils import login_required
from django.db.models import F, Sum, ExpressionWrapper, FloatField
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.db import transaction


@login_required
@csrf_exempt
def guardar_factura(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():  # ⬅️ Aquí
                data = json.loads(request.body)
                usuario_id = request.session['user_id']
                productos = data.get("productos", [])
                cliente = data.get('cliente', 'Generico')
                tipo_pago = data.get('tipo_pago')
            
                efectivo_cordoba = data.get('efectivo_cordoba', 0)
                efectivo_dolar = data.get('efectivo_dolar', 0)
                
                tasa = Opciones.objects.first()
                tasa_cambio = tasa.tasacambio
                
                caja = Cajas.objects.filter(usuarioid=request.session['user_id'], estado=1).first()
                
                if not caja:
                    return JsonResponse({"success": False, "message": "Abra una caja primero"})
                
                factura = Facturas.objects.create(
                    fecha=timezone.now(),
                    usuarioid_id=usuario_id,
                    cliente=cliente,
                    cordobas=efectivo_cordoba,
                    dolares=efectivo_dolar,
                    tipo=tipo_pago,
                    tasacambio=tasa_cambio,
                    cajaid = caja.cajaid,
                    estado=1
                )
                
                for item in productos:
                    tipo = item.get("tipo")
                    cantidad = item.get("cantidad")
                    precio = item.get("precio")
                    
                    if tipo == "farmacia":
                        producto = Productos.objects.get(pk=item.get("id"))
                        
                        restante = cantidad
                        acti = False
                        primer_lote = None

                        while restante > 0:   
                            lote = Lotes.objects.filter(productoid=producto, estado=1).first()

                            if not lote:
                                lote = Lotes.objects.filter(productoid=producto, estado=3).order_by('loteid').first()
                                if lote:
                                    lote.estado = 1  # Activar siguiente lote
                                    lote.save()
                                    acti = True
                                else:
                                    raise Exception(f"No hay suficiente stock para el producto {producto.nombre}")

                            if not primer_lote:
                                primer_lote = lote

                            if lote.stock >= restante:
                                lote.stock -= restante
                                producto.stock -= restante

                                if lote.stock == 0:
                                    lote.estado = 2  # Lote cerrado

                                lote.save()
                                restante = 0
                            else:
                                restante -= lote.stock
                                producto.stock -= lote.stock
                                lote.stock = 0
                                lote.estado = 2
                                lote.save()

                        if acti:
                            lote = Lotes.objects.filter(productoid=producto, estado=1).first()
                            if lote:
                                producto.preciounidad = lote.precioventa

                        producto.save()

                        Detallefacturas.objects.create(
                            facturaid=factura,
                            productoid=producto,
                            cantidad=cantidad,
                            precio=precio,
                            estado=1,
                            preciocompra=primer_lote.preciocompraunitario if primer_lote else 0
                        )

                    else:
                        producto = Productosropa.objects.get(pk=item.get("id"))
                        
                        Detallefacturasropa.objects.create(
                            facturaid=factura,
                            productoropaid=producto,
                            cantidad=cantidad,
                            precio=precio,
                            estado=1,
                            preciocompra=producto.precio
                        )
                
                return JsonResponse({"success": True, "message": "Factura guardada correctamente"})

        except Exception as e:
            return JsonResponse({"success": False, "message": f"Error: {str(e)}"})

    return JsonResponse({"success": False, "message": "Método no permitido"})


@login_required
def nuevaFactura(request):
    user_data = datosUser(request)
    return render(request, 'facturas/nuevaFactura.html', user_data)

@login_required
def anularFactura(request, facturaid):
    factura = Facturas.objects.get(pk=facturaid)
    caja = Cajas.objects.get(cajaid=factura.cajaid)
    if caja.estado == 0:
        messages.warning(request, "La caja de esta factura ha sido cerrada. No se puede anular")
        return redirect('historial_facturas')
    else:
        # Anular la factura
        factura.estado = 0
        factura.save()

        # Detalles de productos farmacia
        detalles_farmacia = Detallefacturas.objects.filter(facturaid=factura, estado=1)
        for detalle in detalles_farmacia:
            producto = detalle.productoid
            cantidad = detalle.cantidad

            # Lote activo para ese producto
            lote = Lotes.objects.filter(productoid=producto, estado=1).first()
            if lote:
                lote.stock += cantidad
                lote.save()

            producto.stock += cantidad
            producto.save()

            detalle.estado = 0
            detalle.save()

        # Detalles de productos ropa
        detalles_ropa = Detallefacturasropa.objects.filter(facturaid=factura, estado=1)
        for detalle in detalles_ropa:
            producto_ropa = detalle.productoropaid
            producto_ropa.save()

            detalle.estado = 0
            detalle.save()
        messages.success(request, "Factura " + str(factura.facturaid) + " Anulada Correctamente.")
        return redirect('historial_facturas')
    
@login_required
def buscar_productos(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "GET":
        query = request.GET.get("q", "")
        tipo = request.GET.get("tipo", "farmacia")

        data = []

        if tipo == "farmacia":
            productos = Productos.objects.filter(nombre__istartswith=query) if query else Productos.objects.none()
            for producto in productos:
                data.append({
                    "id": producto.productoid,
                    "nombre": producto.nombre,
                    "precio": producto.preciounidad,
                    "stock": producto.stock,
                    "descripcion": producto.descripcion,
                    "concentracion": str(producto.concentracion) + " " + str(producto.unidadmedidaid.nombre),
                    "presentacion": producto.presentacionid.nombre,
                    "categoria": producto.categoriaid.nombre,                    
                    "imagen": static('productos/' + str(producto.rutafoto)) if producto.rutafoto else static('productos/noproducto.jpg')
                })

        elif tipo == "tienda":
            productos = Productosropa.objects.filter(nombre__istartswith=query) if query else Productosropa.objects.none()
            for producto in productos:
                data.append({
                    "id": producto.productoropaid,
                    "nombre": producto.nombre,
                    "precio": producto.precio,
                    "talla": producto.talla,
                    "categoria": producto.categoriaropaid.nombre,
                    "descripcion": producto.descripcion,
                    "imagen": static('productos/' + str(producto.rutafoto)) if producto.rutafoto else static('productos/noproducto.jpg')
                })

        
        return JsonResponse({"productos": data})
    
    # Si no es una petición válida, devuelve error JSON
    return JsonResponse({"error": "Peticion invalida"}, status=400)

@login_required
def buscar_producto_por_codigo(request):
    codigo = request.GET.get('codigo')
    tipo = request.GET.get('tipo')

    producto_data = {
        'success': False,
        'imagen': static('productos/noproducto.jpg'),
        'message': '¡Producto no encontrado!'
    }

    # Buscar en Productos (farmacia)
    if tipo == 'farmacia':
        try:
            producto = Productos.objects.select_related('categoriaid', 'presentacionid').get(codigobarra=codigo, estado=1)
            producto_data.update({
                'success': True,
                'id': producto.productoid,
                'nombre': producto.nombre,
                'precio': producto.preciounidad,
                'stock': producto.stock,
                'tipo': 'farmacia',
                'categoria': producto.categoriaid.nombre if producto.categoriaid else 'Sin asignar',
                'presentacion': producto.presentacionid.nombre if producto.presentacionid else 'Sin asignar',
                'imagen': static('productos/' + str(producto.rutafoto)) if producto.rutafoto else static('productos/noproducto.jpg'),
            })
            return JsonResponse(producto_data)
        except Productos.DoesNotExist:
            return JsonResponse(producto_data)

    # Buscar en Productosropa (tienda)
    if tipo == 'tienda':
        try:
            producto_ropa = Productosropa.objects.get(codigobarraropa=codigo, estado=1)
            producto_data.update({
                'success': True,
                'id': producto_ropa.productoropaid,
                'nombre': producto_ropa.nombre,
                'precio': producto_ropa.precio,
                'talla' : producto_ropa.talla,
                'tipo': 'ropa',
                'categoria': producto_ropa.categoriaropaid.nombre if producto_ropa.categoriaropaid else 'Sin asignar',
                'imagen': static('productos/' + str(producto_ropa.rutafoto)) if producto_ropa.rutafoto else static('productos/noproducto.jpg'),
            })
            
            return JsonResponse(producto_data)
        except Productosropa.DoesNotExist:
            return JsonResponse(producto_data)

@login_required
def historialFacturacion(request):
    user_data = datosUser(request)

    if user_data["rolid"] == 1:
        facturas_queryset = Facturas.objects.filter(estado=1).order_by('-facturaid')
    else:
        facturas_queryset = Facturas.objects.filter(estado=1, usuarioid=user_data['userId']).order_by('-facturaid')
    paginator = Paginator(facturas_queryset, 50)
    
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    cont = (page_obj.number - 1) * paginator.per_page + 1
    for factura in page_obj:
        cant_farmacia = Detallefacturas.objects.filter(facturaid=factura).aggregate(total=Sum('cantidad'))['total'] or 0
        cant_ropa = Detallefacturasropa.objects.filter(facturaid=factura).aggregate(total=Sum('cantidad'))['total'] or 0
        factura.cantProductos = cant_farmacia + cant_ropa

        total_farmacia = Detallefacturas.objects.filter(facturaid=factura).annotate(
            total_linea=ExpressionWrapper(F('precio') * F('cantidad'), output_field=FloatField())
        ).aggregate(total=Sum('total_linea'))['total'] or 0

        total_ropa = Detallefacturasropa.objects.filter(facturaid=factura).annotate(
            total_linea=ExpressionWrapper(F('precio') * F('cantidad'), output_field=FloatField())
        ).aggregate(total=Sum('total_linea'))['total'] or 0

        factura.total = total_farmacia + total_ropa
        factura.cont = cont
        cont += 1

    datos = {**user_data, 'facturas': page_obj, 'usuarios': Usuarios.objects.all()}
    return render(request, 'facturas/historial.html', datos)
  
@login_required  
def filtrar_facturas(request):
    usuario_id = request.GET.get('usuario_id')
    filtro_fecha = request.GET.get('filtro_fecha')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    facturas = Facturas.objects.filter(estado=1)

    if usuario_id:
        facturas = facturas.filter(usuarioid__usuarioid=usuario_id).order_by('-facturaid')

    if filtro_fecha:
        hoy = datetime.today().date()
        if filtro_fecha == 'hoy':
            facturas = facturas.filter(fecha__date=hoy).order_by('-facturaid')
        elif filtro_fecha == 'semana':
            inicio_semana = hoy - timedelta(days=hoy.weekday())
            fin_semana = inicio_semana + timedelta(days=6)
            facturas = facturas.filter(fecha__date__range=[inicio_semana, fin_semana]).order_by('-facturaid')
        elif filtro_fecha == 'mes':
            facturas = facturas.filter(fecha__year=hoy.year, fecha__month=hoy.month).order_by('-facturaid')
        elif filtro_fecha == 'anio':
            facturas = facturas.filter(fecha__year=hoy.year).order_by('-facturaid')
        elif filtro_fecha == 'rango' and fecha_inicio and fecha_fin:
            facturas = facturas.filter(fecha__date__range=[fecha_inicio, fecha_fin]).order_by('-facturaid')

    resultados = []
    for factura in facturas:
        cant_farmacia = Detallefacturas.objects.filter(facturaid=factura).aggregate(total=Sum('cantidad'))['total'] or 0
        cant_ropa = Detallefacturasropa.objects.filter(facturaid=factura).aggregate(total=Sum('cantidad'))['total'] or 0
        total_farmacia = Detallefacturas.objects.filter(facturaid=factura).annotate(
            total_linea=ExpressionWrapper(F('precio') * F('cantidad'), output_field=FloatField())
        ).aggregate(total=Sum('total_linea'))['total'] or 0
        total_ropa = Detallefacturasropa.objects.filter(facturaid=factura).annotate(
            total_linea=ExpressionWrapper(F('precio') * F('cantidad'), output_field=FloatField())
        ).aggregate(total=Sum('total_linea'))['total'] or 0

        resultados.append({
            'facturaid': factura.facturaid,
            'usuario': factura.usuarioid.nombre,
            'cliente': factura.cliente,
            'fecha': factura.fecha.strftime('%d/%m/%Y'),
            'hora': factura.fecha.strftime('%H:%M'),
            'cantProductos': cant_farmacia + cant_ropa,
            'total': round(total_farmacia + total_ropa, 2),
        })

    return JsonResponse({'facturas': resultados})
    
@login_required
def detalle_factura_json(request, factura_id):
    factura = Facturas.objects.get(pk=factura_id)

    detalles_f = Detallefacturas.objects.filter(facturaid=factura)
    detalles_r = Detallefacturasropa.objects.filter(facturaid=factura)

    productos = [{
        'nombre': d.productoid.nombre,
        'cantidad': d.cantidad,
        'precio': float(d.precio),
        'subtotal': float(d.cantidad * d.precio),
    } for d in detalles_f]

    productosropa = [{
        'nombre': d.productoropaid.nombre,
        'cantidad': d.cantidad,
        'precio': float(d.precio),
        'subtotal': float(d.cantidad * d.precio),
    } for d in detalles_r]

    total = sum(p['subtotal'] for p in productos + productosropa)
    tasa = float(factura.tasacambio)
    efectivo_cordobas = float(factura.cordobas)
    efectivo_dolares = float(factura.dolares)

    total_entregado = efectivo_cordobas + (efectivo_dolares * tasa)
    cambio = round(total_entregado - total, 2) if total_entregado > total else 0.0

    return JsonResponse({
        'cliente': factura.cliente,
        'fecha': factura.fecha.strftime("%d/%m/%Y %I:%M %p"),
        'nofactura': factura.facturaid,
        'productos': productos,
        'productosropa': productosropa,
        'total': total,
        'tasacambio': tasa,
        'efectivocordobas': efectivo_cordobas,
        'efectivodolares': efectivo_dolares,
        'cambio': cambio,
        'tipopago': factura.tipo  # Agregamos el tipo de pago
    })
 