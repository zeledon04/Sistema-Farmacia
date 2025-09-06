from django.db import models


class Cajas(models.Model):
    cajaid = models.AutoField(db_column='cajaId', primary_key=True, blank=True)  # Field name made lowercase.
    usuarioid = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='usuarioId')  # Field name made lowercase.
    fechaapertura = models.DateTimeField(db_column='fechaApertura', blank=True, null=True)  # Field name made lowercase.
    fechaciere = models.TextField(db_column='fechaCiere', blank=True, null=True)  # Field name made lowercase.
    cordobasinicial = models.FloatField(db_column='cordobasInicial')  # Field name made lowercase.
    dolaresinicial = models.FloatField(db_column='dolaresInicial')  # Field name made lowercase.
    cordobasfinal = models.FloatField(db_column='cordobasFinal', blank=True, null=True)  # Field name made lowercase.
    dolaresfinal = models.FloatField(db_column='dolaresFinal', blank=True, null=True)  # Field name made lowercase.
    totalingresos = models.FloatField(db_column='totalIngresos', blank=True, null=True)  # Field name made lowercase.
    sobrante = models.FloatField(blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)
    faltante = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cajas'
        

class Categoria(models.Model):
    categoriaid = models.AutoField(db_column='categoriaId', primary_key=True, blank=True)  # Field name made lowercase.
    nombre = models.TextField()
    estado = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categoria'


class Categoriaropa(models.Model):
    categoriaropaid = models.AutoField(db_column='categoriaRopaId', primary_key=True, blank=True)  # Field name made lowercase.
    nombre = models.TextField()
    estado = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categoriaRopa'


class Detallefacturas(models.Model):
    detallefacturaid = models.AutoField(db_column='detalleFacturaId', primary_key=True, blank=True)  # Field name made lowercase.
    facturaid = models.ForeignKey('Facturas', models.DO_NOTHING, db_column='facturaId')  # Field name made lowercase.
    productoid = models.ForeignKey('Productos', models.DO_NOTHING, db_column='productoId')  # Field name made lowercase.
    cantidad = models.IntegerField()
    precio = models.FloatField()
    estado = models.IntegerField(blank=True, null=True)
    preciocompra = models.FloatField()

    class Meta:
        managed = False
        db_table = 'detalleFacturas'


class Detallefacturasropa(models.Model):
    detallefacturaropaid = models.AutoField(db_column='detalleFacturaRopaId', primary_key=True, blank=True)  # Field name made lowercase.  
    facturaid = models.ForeignKey('Facturas', models.DO_NOTHING, db_column='facturaId')  # Field name made lowercase.
    productoropaid = models.ForeignKey('Productosropa', models.DO_NOTHING, db_column='productoRopaId')  # Field name made lowercase.
    cantidad = models.IntegerField()
    precio = models.FloatField()
    estado = models.IntegerField(blank=True, null=True)
    preciocompra = models.FloatField()

    class Meta:
        managed = False
        db_table = 'detalleFacturasRopa'
        
        
class Facturas(models.Model):
    facturaid = models.AutoField(db_column='facturaId', primary_key=True, blank=True)  # Field name made lowercase.
    fecha = models.DateTimeField(blank=True, null=True)
    usuarioid = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='usuarioId', blank=True)  # Field name made lowercase.
    estado = models.IntegerField(blank=True, null=True)
    cliente = models.TextField(blank=True, null=True)
    cordobas = models.FloatField(blank=True, null=True)
    dolares = models.FloatField(blank=True, null=True)
    tipo = models.IntegerField(blank=True, null=True)
    tasacambio = models.FloatField(db_column='tasaCambio', blank=True, null=True)
    cajaid = models.TextField(db_column='cajaId', blank=True, null=True)
    motivo = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'facturas'


class Lotes(models.Model):
    loteid = models.AutoField(db_column='loteId', primary_key=True, blank=True)  # Field name made lowercase.
    fecharegistro = models.DateTimeField(db_column='fechaRegistro', blank=True, null=True)  # Field name made lowercase.
    fechavencimiento = models.TextField(db_column='fechaVencimiento')  # Field name made lowercase.
    preciocompraunitario = models.FloatField(db_column='precioCompraUnitario', blank=True, null=True)  # Field name made lowercase.
    precioventa = models.FloatField(db_column='precioVenta', blank=True, null=True)  # Field name made lowercase.
    cantidad = models.IntegerField()
    productoid = models.ForeignKey('Productos', models.DO_NOTHING, db_column='productoId')  # Field name made lowercase.
    proveedorid = models.ForeignKey('Proveedores', models.DO_NOTHING, db_column='proveedorId', blank=True, null=True)  # Field name made lowercase.     
    estado = models.IntegerField(blank=True, null=True)
    stock = models.IntegerField(db_column='stock', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lotes'


class Presentaciones(models.Model):
    presentacionid = models.AutoField(db_column='presentacionId', primary_key=True, blank=True)  # Field name made lowercase.
    nombre = models.TextField()
    estado = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'presentaciones'


class Productos(models.Model):
    productoid = models.AutoField(db_column='productoId', primary_key=True, blank=True)  # Field name made lowercase.
    codigobarra = models.TextField(db_column='codigoBarra', unique=True, blank=True, null=True)  # Field name made lowercase.
    rutafoto = models.TextField(db_column='rutaFoto', blank=True, null=True)  # Field name made lowercase.
    nombre = models.TextField()
    presentacionid = models.ForeignKey(Presentaciones, models.DO_NOTHING, db_column='presentacionId', blank=True, null=True)  # Field name made lowercase.
    concentracion = models.FloatField(blank=True, null=True)
    unidadmedidaid = models.ForeignKey('Unidadmedidas', models.DO_NOTHING, db_column='unidadMedidaId', blank=True, null=True)  # Field name made lowercase.
    descripcion = models.TextField(blank=True, null=True)
    preciounidad = models.FloatField(db_column='precioUnidad')  # Field name made lowercase.
    stock = models.IntegerField()
    categoriaid = models.ForeignKey(Categoria, models.DO_NOTHING, db_column='categoriaId')  # Field name made lowercase.
    estado = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'productos'


class Productosropa(models.Model):
    productoropaid = models.AutoField(db_column='productoRopaId', primary_key=True, blank=True)  # Field name made lowercase.
    codigobarraropa = models.TextField(db_column='codigoBarraRopa', unique=True, blank=True, null=True)  # Field name made lowercase.
    rutafoto = models.TextField(db_column='rutaFoto', blank=True, null=True)  # Field name made lowercase.
    nombre = models.TextField()
    talla = models.TextField()
    descripcion = models.TextField(blank=True, null=True)
    precio = models.FloatField()
    categoriaropaid = models.ForeignKey(Categoriaropa, models.DO_NOTHING, db_column='categoriaRopaId')  # Field name made lowercase.
    estado = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'productosRopa'
        

class Proveedores(models.Model):
    proveedorid = models.AutoField(db_column='proveedorId', primary_key=True, blank=True)  # Field name made lowercase.
    nombre = models.TextField()
    telefono = models.TextField(blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proveedores'


class Roles(models.Model):
    rolid = models.AutoField(db_column='rolId', primary_key=True, blank=True)  # Field name made lowercase.
    nombrerol = models.TextField(db_column='nombreRol')  # Field name made lowercase.
    estado = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'


class Unidadmedidas(models.Model):
    unidadmedidaid = models.AutoField(db_column='unidadMedidaId', primary_key=True, blank=True)  # Field name made lowercase.
    nombre = models.TextField()
    estado = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unidadMedidas'


class Usuarios(models.Model):
    usuarioid = models.AutoField(db_column='usuarioId', primary_key=True, blank=True)  # Field name made lowercase.
    nombre = models.TextField()
    telefono = models.TextField()
    usuario = models.TextField(unique=True)
    contrasena = models.TextField()
    estado = models.IntegerField(blank=True, null=True)
    rolid = models.ForeignKey(Roles, models.DO_NOTHING, db_column='rolId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'usuarios'
        
class Opciones(models.Model):
    opcionid = models.AutoField(db_column='opcionId', primary_key=True, blank=True)  # Field name made lowercase.
    tasacambio = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'opciones'
        
class Denominacionescaja(models.Model):
    denominacioncajaid = models.AutoField(db_column='denominacionCajaId', primary_key=True, blank=True)  
    cajaid = models.ForeignKey('Cajas', models.DO_NOTHING, db_column='cajaId')  
    tipodenominacion = models.IntegerField(db_column='tipoDenominacion')  
    denominacion = models.IntegerField()
    cantidad = models.IntegerField()
    tipomovimiento = models.IntegerField(db_column='tipoMovimiento')  
    estado = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'denominacionescaja'