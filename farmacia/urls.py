from django.urls import path
from .view import facts, productosRopa, productos, caja, ventasPDF, ventasRopaPDF, categorias, categoriasRopa, facturas, lotes, presentaciones, proveedores, inventarioPDF, unidadMedidas, usuarios, InventarioVentasPDF
from .view.charts import ventas_mensuales, ingresos_mensuales, ventas_por_empleado, estado_inventario
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path("logout/", views.logout_view, name="logout"),
    path('Dashboard', views.dashboard, name='dashboard'),
    
    path('Factura/nuevaFactura', facts.nuevaFactura, name='nueva_factura'),
    path('buscar_productos/', facts.buscar_productos, name='buscar_productos'),
    path('buscar-producto-codigo/', facts.buscar_producto_por_codigo, name='buscar_producto_codigo'),
    path('guardar-factura/', facts.guardar_factura, name='guardar_factura'),

    path('Factura/historial', facts.historialFacturacion, name='historial_facturas'),
    path('factura/detalle/<int:factura_id>/', facts.detalle_factura_json, name='detalle_factura_json'),
    path('filtrar_facturas/', facts.filtrar_facturas, name='filtrar_facturas'),
    path('Facturas/anularFactura/<int:facturaid>', facts.anularFactura, name='anularFactura'),
    
    #url de registro de facturas pdf
    path('registroFacturas/pdf/', facturas.registro_factura_pdf, name='registro_factura_pdf'),
    path('registroFacturas/imprimir/', facturas.imprimir_registro_facturas, name='imprimir_registro_facturas'),
    
    # Rutas para Productos Farmacia
    path('Productos/listar', productos.listarProducto, name='listar_producto'),
    path('Productos/agregarProducto', productos.agregarProducto, name='agregar_producto'),
    path('Productos/actualizarProducto/<int:id>', productos.actualizarProducto, name='actualizar_producto'),
    path('Productos/eliminarProducto/<int:id>', productos.eliminarProducto, name='eliminar_Producto'),
    path('Productos/historialVentas', productos.historialVentas, name='historial_ventas'),
    path('filtrar_productos/', productos.filtrar_productos, name='filtrar_productos'),
    path('filtrar-ventas/', productos.filtrar_ventas, name='filtrar_ventas'),
    
        #url de registro de facturas pdf
    path('registroVentas/pdf/', ventasPDF.registro_ventas_pdf, name='registro_ventas_pdf'),
    path('registroVentas/imprimir/', ventasPDF.imprimir_registro_ventas, name='imprimir_registro_ventas'),
    path('inventario/pdf/', InventarioVentasPDF.inventario_pdf, name='inventario_pdf'),
    path('registroInventario/pdf/', InventarioVentasPDF.registro_inventario_pdf, name='registro_inventario_pdf'),
    path("registroInventario", inventarioPDF.imprimir_registro_inventario, name="imprimir_registro_inventario"),
    
    path('registroVentasRopa/pdf/', ventasRopaPDF.registro_ventas_pdf, name='registro_ventasRopa_pdf'),
    path('registroVentasRopa/imprimir/', ventasRopaPDF.imprimir_registro_ventas, name='imprimir_registroRopa_ventas'),
    # Rutas para Lotes
    path('Productos/listarLotes/<int:id>', lotes.listarLotes, name='listar_lotes'),
    path('Productos/agregarLote/<int:id>', lotes.agregarLote, name='agregar_lote'),
    path('Productos/cerrarLote/<int:id>', lotes.cerrarLote, name='cerrar_lote'),
    path('Productos/eliminarLote/<int:id>', lotes.eliminarLote, name='eliminar_lote'),
    
    
    # Rutas para Categorias Farmacia
    path('Categorias/listar', categorias.listarCategorias, name='listar_categorias'),
    path('Categorias/listarInactivas', categorias.listarCategoriasInactivas, name='listar_categorias_inactivas'),
    path('Categorias/agregarCategoria', categorias.agregarCategoria, name='agregar_categoria'),
    path('Categorias/actualizarCategoria/<int:id>', categorias.actualizarCategoria, name='actualizar_categoria'),
    path('Categorias/eliminarCategoria/<int:id>', categorias.eliminarCategoria, name='eliminar_categoria'),
    path('Categorias/activarCategoria/<int:id>', categorias.activarCategoria, name='activar_categoria'),

    # Rutas para Categorias de Ropa
    path('CategoriasRopa/listar', categoriasRopa.listarCategoriasRopa, name='listar_categorias_ropas'),
    path('CategoriasRopa/listarInactivas', categoriasRopa.listarCategoriasRopaInactivas, name='listar_categorias_ropas_inactivas'),
    path('CategoriasRopa/agregarCategoriaRopa', categoriasRopa.agregarCategoriaRopa, name='agregar_categoria_ropa'),
    path('CategoriasRopa/actualizarCategoriaRopa/<int:id>', categoriasRopa.actualizarCategoriaRopa, name='actualizar_categoria_ropa'),
    path('CategoriasRopa/eliminarCategoriaRopa/<int:id>', categoriasRopa.eliminarCategoriaRopa, name='eliminar_categoria_ropa'),
    path('CategoriasRopa/activarCategoriaRopa/<int:id>', categoriasRopa.activarCategoriaRopa, name='activar_categoria_ropa'),
    
    # Rutas para Productos Ropa
    path('Ropa/listar', productosRopa.listarProductoRopa, name='listar_ropa'),
    path('Ropa/agregarProductoRopa', productosRopa.agregarProductoRopa, name='agregar_producto_ropa'),
    path('Ropa/actualizarProductoRopa/<int:id>', productosRopa.actualizarProductoRopa, name='actualizar_producto_ropa'),
    path('eliminarProductoRopa/<int:id>', productosRopa.eliminarProductoRopa, name='eliminar_producto_ropa'),
    path('Productos/historialVentasRopa', productosRopa.historialVentasRopa, name='historial_ventas_ropa'),
    path('filtrar-productos-ropa/', productosRopa.filtrar_productos_ropa, name='filtrar_productos_ropa'),
    
    # Rutas para Ventas Mensuales(Gráfico Dashboard)
    path('api/ventas_mensuales/', ventas_mensuales.api_ventas_mensuales, name='api_ventas_mensuales'),
    # Rutas para Ingresos Mensuales(Gráfico Dashboard)
    path('api/ingresos_mensuales/', ingresos_mensuales.api_ingresos_mensuales, name='api_ingresos_mensuales'),
    # Rutas para Ventas Por Empleado(Gráfico Dashboard)
    path('api/ventas_por_empleado/', ventas_por_empleado.ventas_por_empleado, name='ventas_por_empleado'),
    # Rutas para Estado de Inventario(Gráfico Dashboard)
    path("api/estado_inventario/", estado_inventario.estado_inventario, name="estado_inventario"),
    
    # Rutas para Proveedores
    path('Proveedores/listar', proveedores.listarProveedores, name='listar_proveedores'),
    path('Proveedores/listarInactivos', proveedores.listarProveedoresInactivos, name='listar_proveedores_inactivos'),
    path('Proveedores/agregarProveedor', proveedores.agregarProveedor, name='agregar_proveedor'),
    path('Proveedores/actualizarProveedor/<int:id>', proveedores.actualizarProveedor, name='actualizar_proveedor'),
    path('Proveedores/eliminarProveedor/<int:id>', proveedores.eliminarProveedor, name='eliminar_proveedor'),
    path('Proveedores/activarProveedor/<int:id>', proveedores.activarProveedor, name='activar_proveedor'),
    
    #Rutas para Presentaciones
    path('Presentaciones/listar', presentaciones.listarPresentaciones, name='listar_presentaciones'),
    path('Presentaciones/listarInactivas', presentaciones.listarPresentacionesInactivas, name='listar_presentaciones_inactivas'),
    path('Presentaciones/agregarPresentacion', presentaciones.agregarPresentacion, name='agregar_presentacion'),
    path('Presentaciones/actualizarPresentacion/<int:id>', presentaciones.actualizarPresentacion, name='actualizar_presentacion'),
    path('Presentaciones/eliminarPresentacion/<int:id>', presentaciones.eliminarPresentacion, name='eliminar_presentacion'),
    path('Presentaciones/activarPresentacion/<int:id>', presentaciones.activarPresentacion, name='activar_presentacion'),
    
    #Rutas para Unidad de Medidas
    path('UnidadMedidas/listar', unidadMedidas.listarUnidadMedidas, name='listar_unidad_medidas'),
    path('UnidadMedidas/listarInactivas', unidadMedidas.listarUnidadMedidasInactivas, name='listar_unidad_medidas_inactivas'), 
    path('UnidadMedidas/agregarUnidadMedida', unidadMedidas.agregarUnidadMedida, name='agregar_unidad_medida'),
    path('UnidadMedidas/actualizarUnidadMedida/<int:id>', unidadMedidas.actualizarUnidadMedida, name='actualizar_unidad_medida'),
    path('UnidadMedidas/eliminarUnidadMedida/<int:id>', unidadMedidas.eliminarUnidadMedida, name='eliminar_unidad_medida'),
    path('UnidadMedidas/activarUnidadMedida/<int:id>', unidadMedidas.activarUnidadMedida, name='activar_unidad_medida'),
    
    #Rutas para Usuarios
    path('Usuarios/listar', usuarios.listarUsuarios, name='listar_usuarios'),
    path('Usuarios/listarInactivos', usuarios.listarUsuariosInactivos, name='listar_usuarios_inactivos'),
    path('Usuarios/agregarUsuario', usuarios.agregarUsuario, name='agregar_usuario'),
    path('Usuarios/actualizarUsuario/<int:id>', usuarios.actualizarUsuario, name='actualizar_usuario'),
    path('Usuarios/eliminarUsuario/<int:id>', usuarios.eliminarUsuario, name='eliminar_usuario'),
    path('Usuarios/activarUsuario/<int:id>', usuarios.activarUsuario, name='activar_usuario'),

    path('verificar_caja/', caja.verificar_caja, name='verificar_caja'),
    path('abrir_caja/', caja.abrir_caja, name='abrir_caja'),
    path('cerrar_caja/', caja.cerrar_caja, name='cerrar_caja'),
    path('Cajas/listarCajas', caja.listarCajas, name='listar_cajas'),
    path('Cajas/detalleCaja/<int:cajaid>', caja.detalleCaja, name='detalleCaja'),
    
    path('Opciones/', views.opciones, name='opciones'),
    
    path('api/tasa-cambio/', views.obtener_tasa_cambio, name='tasa_cambio'),
]


