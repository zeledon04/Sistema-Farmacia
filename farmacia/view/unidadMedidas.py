from datetime import date, timedelta

from farmacia.views import datosUser
from ..models import Lotes, Productos, Unidadmedidas, Usuarios
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from ..utils import admin_required, logout_required, login_required

@login_required
def listarUnidadMedidas(request):
    unidadMedidas = Unidadmedidas.objects.filter(estado=1) 
    user_data = datosUser(request) 
    return render(request, 'pages/unidadMedidas/listarUnidadMedidas.html', {**user_data, 'unidadMedidas': unidadMedidas})

@admin_required
def listarUnidadMedidasInactivas(request):
    unidadMedidas = Unidadmedidas.objects.filter(estado=0)
    user_data = datosUser(request)  
    return render(request, 'pages/unidadMedidas/listarUnidadMedidasInactivas.html', {**user_data, 'unidadMedidas': unidadMedidas})

@admin_required
def agregarUnidadMedida(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        
        # Validación de campos
        categoria = Unidadmedidas(
            nombre=nombre,
            estado=1
        )
        categoria.save()
        messages.success(request, "Unidad de Medida agregada correctamente!")
        return redirect('listar_unidad_medidas')
    user_data = datosUser(request)
    return render(request, 'pages/unidadMedidas/agregarUnidadMedida.html', user_data)

@admin_required
def actualizarUnidadMedida(request, id):
    unidadMedida = Unidadmedidas.objects.get(pk=id)
    user_data = datosUser(request)
    datos = {**user_data, 'unidadMedida' : unidadMedida}
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')

        # Actualizar los demás campos
        unidadMedida.nombre = nombre

        unidadMedida.save()

        messages.success(request, "Unidad de Medida actualizada correctamente!")
        return redirect('listar_unidad_medidas')
    return render(request, 'pages/unidadMedidas/actualizarUnidadMedida.html', datos)

@admin_required
def eliminarUnidadMedida(request, id):
    unidadMedidas = get_object_or_404(Unidadmedidas, pk=id)
    unidadMedidas.estado = 0
    unidadMedidas.save()
    messages.success(request, "Unidad de Medida " + unidadMedidas.nombre + " Eliminada Correctamente.")
    return redirect('listar_unidad_medidas')

@admin_required
def activarUnidadMedida(request, id):
    unidadMedidas = get_object_or_404(Unidadmedidas, pk=id)
    unidadMedidas.estado = 1  # Cambia el estado a activo
    unidadMedidas.save()
    messages.success(request, "Unidad de Medida " + unidadMedidas.nombre + " Activada Correctamente.")
    return redirect('listar_unidad_medidas')

