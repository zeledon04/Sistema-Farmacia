CREATE TABLE roles (
    rolId INTEGER PRIMARY KEY AUTOINCREMENT,
    nombreRol TEXT NOT NULL,
    estado INTEGER DEFAULT 1
);

CREATE TABLE usuarios (
    usuarioId INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT NOT NULL,
    usuario TEXT UNIQUE NOT NULL,
    contrasena TEXT NOT NULL,
    estado INTEGER DEFAULT 1,
    rolId INTEGER NOT NULL,
    FOREIGN KEY (rolId) REFERENCES roles(rolId)
);

CREATE TABLE categoriaRopa (
    categoriaRopaId INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    estado INTEGER DEFAULT 1
);

CREATE TABLE productosRopa (
    productoRopaId INTEGER PRIMARY KEY AUTOINCREMENT,
	codigoBarraRopa text UNIQUE,
	rutaFoto text,
    nombre TEXT NOT NULL,
	talla text not null,
    descripcion TEXT,
    precio REAL NOT NULL,
    categoriaRopaId INTEGER not NULL,
    estado INTEGER DEFAULT 1,
    updated_at Text,
    FOREIGN KEY (categoriaRopaId) REFERENCES categoriaRopa(categoriaRopaId)
);

CREATE INDEX idx_productosRopa_codigoBarra ON productosRopa(codigoBarraRopa);

CREATE TABLE categoria (
    categoriaId INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    estado INTEGER DEFAULT 1
);

CREATE TABLE proveedores (
    proveedorId INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT,
    estado INTEGER DEFAULT 1
);

create table presentaciones (
	presentacionId INTEGER PRIMARY KEY AUTOINCREMENT,
	nombre text not null,
	estado INTEGER DEFAULT 1
);

create table unidadMedidas (
	unidadMedidaId integer primary key AUTOINCREMENT,
	nombre text not null,
	estado integer DEFAULT 1
);

CREATE TABLE productos (
    productoId INTEGER PRIMARY KEY AUTOINCREMENT,
	codigoBarra text UNIQUE,
	rutaFoto text,
    nombre TEXT NOT NULL,
	presentacionId integer,
	concentracion real,
	unidadMedidaId INTEGER,
    descripcion TEXT,
    precioUnidad REAL NOT NULL,
	stock integer not null,
    categoriaId INTEGER not NULL,
    estado INTEGER DEFAULT 1,
    updated_at text, 
    FOREIGN KEY (categoriaId) REFERENCES categoria(categoriaId),
	FOREIGN KEY (presentacionId) REFERENCES presentaciones(presentacionId),
	FOREIGN KEY (unidadMedidaId) REFERENCES unidadMedidas(unidadMedidaId)
);

CREATE INDEX idx_productos_codigoBarra ON productos(codigoBarra);
CREATE INDEX idx_productos_nombre ON productos(nombre COLLATE NOCASE);


CREATE TABLE lotes (
    loteId INTEGER PRIMARY KEY AUTOINCREMENT,
    fechaRegistro DATETIME DEFAULT CURRENT_TIMESTAMP,
    fechaVencimiento TEXT NOT NULL,
    precioCompraUnitario REAL,
    precioVenta real,
    cantidad INTEGER NOT NULL,
    productoId INTEGER NOT NULL,
    proveedorId INTEGER,
    estado INTEGER DEFAULT 1,
    FOREIGN KEY (productoId) REFERENCES productos(productoId),
    FOREIGN KEY (proveedorId) REFERENCES proveedores(proveedorId)
);

CREATE TABLE facturas (
    facturaId INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    usuarioId INTEGER,
    estado INTEGER DEFAULT 1,
    cliente text,
    cordobas real,
    dolares real,
    tipo integer,
    tasacambio real,
    cajaId Text,
    motivo text,
    FOREIGN KEY (usuarioId) REFERENCES usuarios(usuarioId)
);

CREATE TABLE detalleFacturas (
    detalleFacturaId INTEGER PRIMARY KEY AUTOINCREMENT,
    facturaId INTEGER NOT NULL,
    productoId INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL,
    estado INTEGER DEFAULT 1,
    FOREIGN KEY (facturaId) REFERENCES facturas(facturaId),
    FOREIGN KEY (productoId) REFERENCES productos(productoId)
);

CREATE TABLE detalleFacturasRopa (
    detalleFacturaRopaId INTEGER PRIMARY KEY AUTOINCREMENT,
    facturaId INTEGER NOT NULL,
    productoRopaId INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL,
    estado INTEGER DEFAULT 1,
    FOREIGN KEY (facturaId) REFERENCES facturas(facturaId),
    FOREIGN KEY (productoRopaId) REFERENCES productosRopa(productoRopaId)
);


create table cajas (
	cajaId INTEGER PRIMARY KEY AUTOINCREMENT,
	usuarioId INTEGER not null,
	fechaApertura DATETIME DEFAULT CURRENT_TIMESTAMP,
	fechaCiere DATETIME DEFAULT CURRENT_TIMESTAMP,
	cordobasInicial real not null,
	dolaresInicial real not null,
	cordobasFinal real,
	dolaresFinal real,
	totalIngresos real,
	sobrante real,
	estado INTEGER DEFAULT 1,
	FOREIGN KEY (usuarioId) REFERENCES usuarios(usuarioId)
);

CREATE TABLE denominacionesCaja (
    denominacionCajaId INTEGER PRIMARY KEY AUTOINCREMENT,
    cajaId INTEGER NOT NULL,
    tipoDenominacion INTEGER NOT NULL, -- 1 = Córdobas, 2 = Dólares
    denominacion INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    tipoMovimiento INTEGER NOT NULL, -- 1 = Apertura, 2 = Cierre
    estado INTEGER DEFAULT 1,
    FOREIGN KEY (cajaId) REFERENCES cajas(cajaId)
);

INSERT INTO roles (nombreRol) VALUES
('Administrador'),
('Cajero');

INSERT INTO usuarios (nombre, telefono, usuario, contrasena, rolId) VALUES
('Jair Hernandez', '8888-1234', 'JairHC', '1234', 1),
('Eduardo Zeledon', '8888-5678', 'EduZel', '1234', 2);

INSERT INTO categoriaRopa (nombre) VALUES
('Blusas'),
('Pantalones'),
('Ropa Interior');

INSERT INTO productosRopa (codigoBarraRopa, rutaFoto, nombre, talla, descripcion, precio, categoriaRopaId) VALUES
('7501035907584', 'camisa1.jpg', 'Camisa Azul', 'M', 'Camisa de algodón manga larga', 12.99, 1),
('027084120134', 'pantalon1.jpg', 'Pantalón Negro', 'L', 'Pantalón de mezclilla', 18.50, 2),
('9789996443206', 'interior.jpg', 'Bragas', 'S', 'Bragas roja de encaje', 25.00, 3);

INSERT INTO categoria (nombre) VALUES
('Analagesico'),
('Vitaminas'),
('antialergico');

INSERT INTO presentaciones (nombre) VALUES
('Tabletas'),
('Jarabe'),
('Ampoya');

INSERT INTO unidadMedidas (nombre) VALUES
('mg'),
('ml'),
('g');

INSERT INTO productos (codigoBarra, rutaFoto, nombre, presentacionId, concentracion, unidadMedidaId, descripcion, precioUnidad, stock, categoriaId) VALUES
('6948154234923', 'paracetamol.jpg', 'Paracetamol', 1, 500, 1, 'Analgésico y antipirético', 2, 0, 1),
('751492638362', 'vitaminaC.jpg', 'Vitamina C', 2, 100, 2, 'Vitamina para fortalecer el sistema inmune', 75, 0, 2),
('731809001997', 'loratadinaInye.jpg', 'Loratadina en apoya', 2, 5, 2, 'Antialergico Inyectable', 18, 0, 3);

INSERT INTO proveedores (nombre, telefono) VALUES
('Saba', '2222-3333'),
('Samaria', '2222-4354'),
('Paisanos', '3333-4444');

INSERT INTO lotes (fechaVencimiento, precioCompraUnitario, precioCompraLote, cantidad, productoId, proveedorId) VALUES
('2025-12-31', 0.90, 180, 200, 1, 1),
('2026-05-20', 65, 1950, 30, 2, 2),
('2025-10-01', 12, 600, 35, 3, 3);

INSERT INTO facturas (usuarioId) VALUES
(1),
(2);

INSERT INTO detalleFacturas (facturaId, productoId, cantidad, precio) VALUES
(1, 1, 5, 10),
(1, 2, 1, 75),
(2, 3, 1, 18);


SELECT * FROM productos