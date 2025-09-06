
from farmacia.views import datosUser
from ..models import Categoriaropa
from django.shortcuts import get_object_or_404, redirect, render
from ..utils import admin_required, login_required
from django.contrib import messages

@login_required
def listarCategoriasRopa(request):
    user_data = datosUser(request)
    categoriasRopa = Categoriaropa.objects.filter(estado=1)  
    return render(request, 'pages/categoriasRopa/listarCategoriasRopa.html', {**user_data, 'categoriasRopa': categoriasRopa})

@admin_required
def listarCategoriasRopaInactivas(request):
    categoriasRopa = Categoriaropa.objects.filter(estado=0)
    user_data = datosUser(request) 
    return render(request, 'pages/categoriasRopa/listarCategoriasRopaInactivas.html', {**user_data, 'categoriasRopa': categoriasRopa})

@admin_required
def agregarCategoriaRopa(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        
        # Validación de campos
        categoriasRopa = Categoriaropa(
            nombre=nombre,
            estado=1
        )
        categoriasRopa.save()
        messages.success(request, "Categoría de Ropa agregada correctamente!")
        return redirect('listar_categorias_ropas')
    user_data = datosUser(request)
    return render(request, 'pages/categoriasRopa/agregarCategoriaRopa.html', user_data)

@admin_required
def actualizarCategoriaRopa(request, id):
    categoriaropa = Categoriaropa.objects.get(pk=id)
    user_data = datosUser(request)
    datos = {**user_data, 'categoriaropa' : categoriaropa}
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')

        # Actualizar los demás campos
        categoriaropa.nombre = nombre

        categoriaropa.save()

        messages.success(request, "Categoría de Ropa actualizada correctamente!")
        return redirect('listar_categorias_ropas')
    
    return render(request, 'pages/categoriasRopa/actualizarCategoriaRopa.html', datos)

@admin_required
def eliminarCategoriaRopa(request, id):
    categoriaRopa = get_object_or_404(Categoriaropa, pk=id)
    categoriaRopa.estado = 0
    categoriaRopa.save()
    messages.success(request, "Categoría de Ropa" + categoriaRopa.nombre + " Eliminada Correctamente.")
    return redirect('listar_categorias_ropas')

@admin_required
def activarCategoriaRopa(request, id):
    categoriaRopa = get_object_or_404(Categoriaropa, pk=id)
    categoriaRopa.estado = 1  # Cambia el estado a activo
    categoriaRopa.save()
    messages.success(request, "Categoría de Ropa" + categoriaRopa.nombre + " Activada Correctamente.")
    return redirect('listar_categorias_ropas')

