
from farmacia.views import datosUser
from ..models import Presentaciones
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from ..utils import admin_required, login_required

@login_required
def listarPresentaciones(request):
    presentaciones = Presentaciones.objects.filter(estado=1)  
    user_data = datosUser(request)
    return render(request, 'pages/presentaciones/listarPresentaciones.html', {**user_data, 'presentaciones': presentaciones})

@admin_required
def listarPresentacionesInactivas(request):
    presentaciones = Presentaciones.objects.filter(estado=0)  
    user_data = datosUser(request)
    return render(request, 'pages/presentaciones/listarPresentacionesInactivas.html', {**user_data, 'presentaciones': presentaciones})

@admin_required
def agregarPresentacion(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        
        # Validación de campos
        presentacion = Presentaciones(
            nombre=nombre,
            estado=1
        )
        presentacion.save()
        messages.success(request, "Presentación agregada correctamente!")
        return redirect('listar_presentaciones')
    user_data = datosUser(request)
    return render(request, 'pages/presentaciones/agregarPresentacion.html', user_data)

@admin_required
def actualizarPresentacion(request, id):
    presentacion = Presentaciones.objects.get(pk=id)
    user_data = datosUser(request)
    datos = {**user_data, 'presentacion' : presentacion}
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')

        # Actualizar los demás campos
        presentacion.nombre = nombre

        presentacion.save()

        messages.success(request, "Presentación actualizada correctamente!")
        return redirect('listar_presentaciones')
    return render(request, 'pages/presentaciones/actualizarPresentacion.html', datos)

@admin_required
def eliminarPresentacion(request, id):
    presentacion = get_object_or_404(Presentaciones, pk=id)
    presentacion.estado = 0
    presentacion.save()
    messages.success(request, "Presentación " + presentacion.nombre + " Eliminada Correctamente.")
    return redirect('listar_presentaciones')

@admin_required
def activarPresentacion(request, id):
    presentacion = get_object_or_404(Presentaciones, pk=id)
    presentacion.estado = 1  # Cambia el estado a activo
    presentacion.save()
    messages.success(request, "Presentación " + presentacion.nombre + " Activada Correctamente.")
    return redirect('listar_presentaciones')

