function eliminarProducto(id){
    Swal.fire({
        "title": "¿Estás seguro?",
        "icon": "question",
        "showCancelButton": true,
        "cancelButtonText": "No, Cancelar",
        "confirmButtonText": "Si, Eliminar",
        "reverseButtons":true,
        "confirmButtonColor": "#dc3545"
    })
        .then(function(result){
            if (result.isConfirmed){
                 window.location.href = "/Productos/eliminarProducto/"+id
            }
        })
}

function eliminarProductoRopa(id){
    Swal.fire({
        "title": "¿Estás segurodd?",
        "icon": "question",
        "showCancelButton": true,
        "cancelButtonText": "No, Cancelar",
        "confirmButtonText": "Si, Eliminar",
        "reverseButtons":true,
        "confirmButtonColor": "#dc3545"
    })
        .then(function(result){
            if (result.isConfirmed){
                 window.location.href = "/eliminarProductoRopa/"+id
            }
        })
}

function eliminarCategoria(id){
    Swal.fire({
        "title": "¿Estás seguro?",
        "icon": "question",
        "showCancelButton": true,
        "cancelButtonText": "No, Cancelar",
        "confirmButtonText": "Si, Eliminar",
        "reverseButtons":true,
        "confirmButtonColor": "#dc3545"
    })
        .then(function(result){
            if (result.isConfirmed){
                 window.location.href = "/Categorias/eliminarCategoria/"+id
            }
        })
}

function eliminarCategoriaRopa(id){
    Swal.fire({
        "title": "¿Estás seguro?",
        "icon": "question",
        "showCancelButton": true,
        "cancelButtonText": "No, Cancelar",
        "confirmButtonText": "Si, Eliminar",
        "reverseButtons":true,
        "confirmButtonColor": "#dc3545"
    })
        .then(function(result){
            if (result.isConfirmed){
                 window.location.href = "/CategoriasRopa/eliminarCategoriaRopa/"+id
            }
        })
}

function eliminarPresentacion(id){
    Swal.fire({
        "title": "¿Estás seguro?",
        "icon": "question",
        "showCancelButton": true,
        "cancelButtonText": "No, Cancelar",
        "confirmButtonText": "Si, Eliminar",
        "reverseButtons":true,
        "confirmButtonColor": "#dc3545"
    })
        .then(function(result){
            if (result.isConfirmed){
                 window.location.href = "/Presentaciones/eliminarPresentacion/"+id
            }
        })
}

function eliminarProveedor(id){
    Swal.fire({
        "title": "¿Estás seguro?",
        "icon": "question",
        "showCancelButton": true,
        "cancelButtonText": "No, Cancelar",
        "confirmButtonText": "Si, Eliminar",
        "reverseButtons":true,
        "confirmButtonColor": "#dc3545"
    })
        .then(function(result){
            if (result.isConfirmed){
                 window.location.href = "/Proveedores/eliminarProveedor/"+id
            }
        })
}

function eliminarUnidadMedida(id){
    Swal.fire({
        "title": "¿Estás seguro?",
        "icon": "question",
        "showCancelButton": true,
        "cancelButtonText": "No, Cancelar",
        "confirmButtonText": "Si, Eliminar",
        "reverseButtons":true,
        "confirmButtonColor": "#dc3545"
    })
        .then(function(result){
            if (result.isConfirmed){
                 window.location.href = "/UnidadMedidas/eliminarUnidadMedida/"+id
            }
        })
}

function eliminarUsuario(id){
    Swal.fire({
        "title": "¿Estás seguro?",
        "icon": "question",
        "showCancelButton": true,
        "cancelButtonText": "No, Cancelar",
        "confirmButtonText": "Si, Eliminar",
        "reverseButtons":true,
        "confirmButtonColor": "#dc3545"
    })
        .then(function(result){
            if (result.isConfirmed){
                 window.location.href = "/Usuarios/eliminarUsuario/"+id
            }
        })
}

function eliminarLote(id){
    Swal.fire({
        "title": "¿Estás seguro?",
        "icon": "question",
        "showCancelButton": true,
        "cancelButtonText": "No, Cancelar",
        "confirmButtonText": "Si, Eliminar",
        "reverseButtons":true,
        "confirmButtonColor": "#dc3545"
    })
        .then(function(result){
            if (result.isConfirmed){
                 window.location.href = "/Productos/eliminarLote/"+id
            }
        })
}