from datetime import date, timedelta

from farmacia.views import datosUser
from ..models import Lotes, Productos, Proveedores, Usuarios
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from ..utils import admin_required, login_required

@login_required
def listarProveedores(request):
    proveedores = Proveedores.objects.filter(estado=1) 
    user_data = datosUser(request)
    return render(request, 'pages/proveedores/listarProveedores.html', {**user_data, 'proveedores': proveedores})

@admin_required
def listarProveedoresInactivos(request):
    proveedores = Proveedores.objects.filter(estado=0) 
    user_data = datosUser(request)
    return render(request, 'pages/proveedores/listarProveedoresInactivos.html', {**user_data, 'proveedores': proveedores})

@admin_required
def agregarProveedor(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono')
        
        # Validación de campos
        proveedor = Proveedores(
            nombre=nombre,
            telefono=telefono,
            estado=1
        )
        proveedor.save()
        messages.success(request, "Provedor agregado correctamente!")
        return redirect('listar_proveedores')
    user_data = datosUser(request)
    return render(request, 'pages/proveedores/agregarProveedor.html', user_data)

@admin_required
def actualizarProveedor(request, id):
    proveedor = Proveedores.objects.get(pk=id)
    user_data = datosUser(request)
    datos = {**user_data, 'proveedor' : proveedor}
    
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre')
            telefono = request.POST.get('telefono')
        except Proveedores.DoesNotExist:
            messages.error(request, "Proveedor no encontrado.")
            return redirect('listar_proveedores')
    

        # Actualizar los demás campos
        proveedor.nombre = nombre
        proveedor.telefono = telefono

        proveedor.save()

        messages.success(request, "Proveedor actualizado correctamente!")
        return redirect('listar_proveedores')
    return render(request, 'pages/proveedores/actualizarProveedor.html', datos)

@admin_required
def eliminarProveedor(request, id):
    proveedor = get_object_or_404(Proveedores, pk=id)
    proveedor.estado = 0
    proveedor.save()
    messages.success(request, "Proveedor " + proveedor.nombre + " Eliminado Correctamente.")
    return redirect('listar_proveedores')

@admin_required
def activarProveedor(request, id):
    proveedor = get_object_or_404(Proveedores, pk=id)
    proveedor.estado = 1  # Cambia el estado a activo
    proveedor.save()
    messages.success(request, "Proveedor " + proveedor.nombre + " Activado Correctamente.")
    return redirect('listar_proveedores')

