from datetime import date, timedelta

from farmacia.views import datosUser
from ..models import Lotes, Productos, Usuarios, Roles
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from ..utils import admin_required, logout_required, login_required

@login_required
def listarUsuarios(request):
    user_data = datosUser(request)
    usuarios = Usuarios.objects.filter(estado=1)  
    return render(request, 'pages/usuarios/listarUsuarios.html', {**user_data, 'usuarios': usuarios})

@admin_required
def listarUsuariosInactivos(request):
    user_data = datosUser(request)
    usuarios = Usuarios.objects.filter(estado=0).select_related('rolid')  # Usar select_related para optimizar la consulta    
    return render(request, 'pages/usuarios/listarUsuariosInactivos.html', {**user_data, 'usuarios': usuarios})

@admin_required
def agregarUsuario(request):
    roles = Roles.objects.filter(estado = 1)
    user_data = datosUser(request)
    datos = {**user_data, 'roles' : roles}
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        rolid = request.POST.get('rolid')
        usuario = request.POST.get('usuario')
        contrasena = request.POST.get('contrasena')
        telefono = request.POST.get('telefono')
        
        # Validación de campos
        usuario = Usuarios(
            nombre=nombre,
            rolid_id=rolid,
            usuario=usuario,
            contrasena=contrasena,
            telefono=telefono,
            estado=1
        )
        usuario.save()
        messages.success(request, "Usuario agregado correctamente!")
        return redirect('listar_usuarios')
    return render(request, 'pages/usuarios/agregarUsuario.html', datos)

@admin_required
def actualizarUsuario(request, id):
    roles = Roles.objects.filter(estado = 1)
    usuario = Usuarios.objects.get(pk=id)
    user_data = datosUser(request)
    datos = {**user_data, 'usuario' : usuario, 'roles' : roles}
    
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre')
            rolid = request.POST.get('rolid')
            usuarioNombre = request.POST.get('usuario')
            contrasena = request.POST.get('contrasena')
            telefono = request.POST.get('telefono')
        except Usuarios.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")
            return redirect('listar_usuarios')
    
        if rolid is None:
            rolid = usuario.rolid_id  # Mantener el rol actual si no se proporciona uno nuevo
        print("Rol ID:", rolid)  # Depuración: Verificar el valor de rolid
        
        # Actualizar los demás campos
        usuario.nombre = nombre
        usuario.telefono = telefono
        usuario.usuario = usuarioNombre
        usuario.contrasena = contrasena
        usuario.rolid_id = rolid

        usuario.save()

        messages.success(request, "Usuario actualizado correctamente!")
        return redirect('listar_usuarios')
    return render(request, 'pages/usuarios/actualizarUsuario.html', datos)

@admin_required
def eliminarUsuario(request, id):
    usuario = get_object_or_404(Usuarios, pk=id)
    user_data = datosUser(request)
    if id == user_data.get('userId'):
        messages.error(request, "No puedes eliminar tu propio usuario.")
        return redirect('listar_usuarios')
    usuario.estado = 0
    usuario.save()
    messages.success(request, "Usuario " + usuario.nombre + " Eliminado Correctamente.")
    return redirect('listar_usuarios')

@admin_required
def activarUsuario(request, id):
    usuario = get_object_or_404(Usuarios, pk=id)
    usuario.estado = 1  # Cambia el estado a activo
    usuario.save()
    messages.success(request, "Usuario " + usuario.nombre + " Activado Correctamente.")
    return redirect('listar_usuarios')
