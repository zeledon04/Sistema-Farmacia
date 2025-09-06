let tipoProducto = "farmacia";

document.addEventListener('DOMContentLoaded', function () {
    
    const btnFarmacia = document.getElementById('btnFarmacia');
    const btnTienda = document.getElementById('btnTienda');

    btnFarmacia.addEventListener('click', function () {
        tipoProducto = 'farmacia';
        const valorBuscador = document.getElementById('buscador').value;
        buscarProductos(valorBuscador);
        activarBoton(this);
    });

    btnTienda.addEventListener('click', function () {
        tipoProducto = 'tienda';
        const valorBuscador = document.getElementById('buscador').value;
        buscarProductos(valorBuscador);
        activarBoton(this);
    });

    document.getElementById('buscador').addEventListener('input', function() {
        buscarProductos(this.value);
    });

    document.addEventListener('click', function(e) {
        const target = e.target.closest('.ver-detalles'); // busca el elemento más cercano con esa clase

        if (target) {
            if (tipoProducto == 'farmacia') {
                e.preventDefault();
                e.stopPropagation();

                const nombre = target.getAttribute('data-nombre');
                const categoria = target.getAttribute('data-categoria');
                const presentacion = target.getAttribute('data-presentacion');
                const concentracion = target.getAttribute('data-concentracion');
                const descripcion = target.getAttribute('data-descripcion');
                const imagen = target.getAttribute('data-imagen');

                Swal.fire({
                title: nombre,
                text: descripcion,
                html: `
                    <img src="${imagen}" alt="${nombre}" class="w-40 h-40 object-contain mx-auto mb-4 rounded" />
                    <p><strong>Categoria:</strong> ${categoria}</p>
                    <p><strong>presentacion:</strong> ${presentacion}</p>
                    <p><strong>concentracion:</strong> ${concentracion}</p>
                    <p><strong>Descripción:</strong> ${descripcion}</p>
                `,
                confirmButtonText: 'Cerrar',
                width: 400
                });
            } else {
                e.preventDefault();
                e.stopPropagation();

                const nombre = target.getAttribute('data-nombre');
                const categoria = target.getAttribute('data-categoria');
                const talla = target.getAttribute('data-talla');
                const descripcion = target.getAttribute('data-descripcion');
                const imagen = target.getAttribute('data-imagen');

                Swal.fire({
                title: nombre,
                text: descripcion,
                html: `
                    <img src="${imagen}" alt="${nombre}" class="w-40 h-40 object-contain mx-auto mb-4 rounded" />
                    <p><strong>Categoria:</strong> ${categoria}</p>
                    <p><strong>Talla:</strong> ${talla}</p>
                    <p><strong>Descripción:</strong> ${descripcion}</p>
                `,
                confirmButtonText: 'Cerrar',
                width: 400
                });
            }
        }
    });


    document.addEventListener('click', function(e) {
        const btn = e.target.closest('.agregar-btn');
        if (!btn) return;

        const productoid = btn.getAttribute('data-id');
       
        const nombre = btn.getAttribute('data-nombre');
        const precio = parseFloat(btn.getAttribute('data-precio')).toFixed(2);
        const tbody = document.getElementById('cuerpo-factura');
        const stock = btn.getAttribute('data-stock')
        

        // Buscar fila existente por data-nombre
        const filaExistente = tbody.querySelector(`tr[data-nombre="${CSS.escape(nombre)}"]`);

        if (filaExistente) {
            const cantidadInput = filaExistente.querySelector('.cantidad');
            let cantidad = parseInt(cantidadInput.value) + 1;
            cantidadInput.value = cantidad;

            const precioInput = filaExistente.querySelector('.precio');
            const nuevoPrecio = parseFloat(precioInput.value);
            const nuevoSubtotal = (cantidad * nuevoPrecio).toFixed(2);
            console.log(nuevoSubtotal);
            filaExistente.querySelector('.subtotal').textContent = `C$ ${nuevoSubtotal}`;

            actualizarTotal();
        
        } else {
            // Crear nuevo tr
            const nuevaFila = document.createElement('tr');
            nuevaFila.setAttribute('data-id', productoid);
            nuevaFila.setAttribute('data-nombre', nombre);
            nuevaFila.setAttribute('data-tipo', tipoProducto);
            
            if (tipoProducto == 'farmacia') {
                nuevaFila.setAttribute('data-stock', stock);
            }

            const maxAttr = tipoProducto == 'farmacia' ? `max="${stock}"` : '';

            nuevaFila.innerHTML = `
            <td class="text-center px-2 py-1 font-semibold">1</td>
            <td class="text-center px-2 py-1 font-semibold">${nombre}</td>
            <td class="text-center px-2 py-1">
                <input type="number" ${maxAttr} min="1" value="1" class="cantidad w-14 text-center border rounded" />
            </td>
            <td class="text-center px-2 py-1">
                C$<input type="number" min="1" value="${precio}" class="precio w-20 text-center border rounded" />
            </td>
            <td class="text-center px-2 py-1 subtotal font-semibold">C$ ${precio}</td>
            <td class="text-center px-2 py-1">
                <button class="text-red-600 hover:text-red-800 eliminar-item">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                        stroke-width="1.5" stroke="currentColor" class="size-6 text-red-500">
                        <path stroke-linecap="round" stroke-linejoin="round" 
                        d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 
                        1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 
                        1-2.244 2.077H8.084a2.25 2.25 0 0 
                        1-2.244-2.077L4.772 5.79m14.456 
                        0a48.108 48.108 0 0 0-3.478-.397m-12 
                        .562c.34-.059.68-.114 1.022-.165m0 
                        0a48.11 48.11 0 0 1 3.478-.397m7.5 
                        0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 
                        51.964 0 0 0-3.32 0c-1.18.037-2.09 
                        1.022-2.09 2.201v.916m7.5 
                        0a48.667 48.667 0 0 0-7.5 0" />
                    </svg>  
                </button>
            </td>
            `;
            tbody.appendChild(nuevaFila);
            actualizarTotal();
        }
    });

    document.addEventListener('input', function(e) {
        if (!e.target.classList.contains('cantidad') && !e.target.classList.contains('precio')) return;

        const fila = e.target.closest('tr');
        if (!fila) return;

        const cantidadInput = fila.querySelector('.cantidad');
        const precioInput = fila.querySelector('.precio');

        const cantidad = parseInt(cantidadInput?.value) || 1;
        const precio = parseFloat(precioInput?.value) || 0;

        const subtotal = (cantidad * precio).toFixed(2);
        const subtotalElem = fila.querySelector('.subtotal');
        if (subtotalElem) {
            subtotalElem.textContent = `$${subtotal}`;
        }

        actualizarTotal();
    });

    document.addEventListener('click', function(e) {
        if (!e.target.closest('.eliminar-item')) return;

        const btnEliminar = e.target.closest('.eliminar-item');
        const fila = btnEliminar.closest('tr');
        if (fila) {
            fila.remove();
            actualizarTotal();
        }
    });

    const inputCodigo = document.getElementById('input-codigo-barra');
    
    inputCodigo.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            const codigo = inputCodigo.value.trim();
            if (!codigo) return;
            const tipoo = tipoProducto
            fetch(`/buscar-producto-codigo/?codigo=${encodeURIComponent(codigo)}&tipo=${tipoo}`)
                .then(response => response.json())
                .then(data => {
                    if (!data.success) {
                        Swal.fire({
                            icon : 'error',
                            title : data.message
                        });
                    } else {
                        agregarProductoAFactura(data);
                    }
                    inputCodigo.value = '';
                })
                .catch(error => {
                    console.error('Error en la solicitud:', error);
                    alert('Error del servidor. Intenta de nuevo.');
                    inputCodigo.value = '';
                });
        }
    });


});

function agregarProductoAFactura(producto) {
    const productoid = producto.id;
    console.log(producto);
    const tbody = document.getElementById('cuerpo-factura');
    const nombre = producto.nombre;
    const precio = parseFloat(producto.precio).toFixed(2);
    const stock = producto.stock;

    // Verificar si ya existe una fila con este nombre
    const filaExistente = Array.from(tbody.querySelectorAll('tr')).find(
        tr => tr.dataset.nombre === nombre
    );

    if (filaExistente) {
        // Incrementar cantidad si ya está en la tabla
        const cantidadInput = filaExistente.querySelector('.cantidad');
        let cantidad = parseInt(cantidadInput.value) + 1;
        cantidadInput.value = cantidad;

        const nuevoPrecio = parseFloat(filaExistente.querySelector('.precio').value);
        const nuevoSubtotal = (cantidad * nuevoPrecio).toFixed(2);
        filaExistente.querySelector('.subtotal').textContent = `C$ ${nuevoSubtotal}`;
    } else {
        // Crear nueva fila si no existe
        const nuevaFila = document.createElement('tr');
        nuevaFila.setAttribute('data-id', productoid);
        nuevaFila.setAttribute('data-nombre', nombre);
        nuevaFila.setAttribute('data-tipo', tipoProducto);

        if (tipoProducto == 'farmacia') {
            nuevaFila.setAttribute('data-stock', stock);
        }
        const maxAttr = tipoProducto === 'farmacia' ? `max="${stock}"` : '';

        nuevaFila.innerHTML = `
            <td class="text-center px-2 py-1 font-semibold">1</td>
            <td class="text-center px-2 py-1 font-semibold">${nombre}</td>
            <td class="text-center px-2 py-1">
                <input type="number" ${maxAttr} min="1" value="1" class="cantidad w-14 text-center border rounded" />
            </td>
            <td class="text-center px-2 py-1">
                C$<input type="number" min="1" value="${precio}" class="precio w-20 text-center border rounded" />
            </td>
            <td class="text-center px-2 py-1 subtotal font-semibold">C$ ${precio}</td>
            <td class="text-center px-2 py-1">
                <button class="text-red-600 hover:text-red-800 eliminar-item">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" 
                        stroke-width="1.5" stroke="currentColor" class="size-6 text-red-500">
                        <path stroke-linecap="round" stroke-linejoin="round" 
                              d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 
                              1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 
                              1-2.244 2.077H8.084a2.25 2.25 0 0 
                              1-2.244-2.077L4.772 5.79m14.456 
                              0a48.108 48.108 0 0 0-3.478-.397m-12 
                              .562c.34-.059.68-.114 1.022-.165m0 
                              0a48.11 48.11 0 0 1 3.478-.397m7.5 
                              0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 
                              51.964 0 0 0-3.32 0c-1.18.037-2.09 
                              1.022-2.09 2.201v.916m7.5 
                              0a48.667 48.667 0 0 0-7.5 0" />
                    </svg>
                </button>
            </td>
        `;
        tbody.appendChild(nuevaFila);
    }

    actualizarTotal();
}



function actualizarTotal() {
    let total = 0;
    const filas = document.querySelectorAll('#cuerpo-factura tr');
    
    filas.forEach(fila => {
        const cantidadInput = fila.querySelector('.cantidad');
        const precioInput = fila.querySelector('.precio');
        
        const cantidad = cantidadInput ? parseFloat(cantidadInput.value) || 0 : 0;
        const precio = precioInput ? parseFloat(precioInput.value) || 0 : 0;
        
        total += cantidad * precio;
    });

    const totalFinal = document.getElementById('total-final');
    if (totalFinal) {
        totalFinal.textContent = `C$${total.toFixed(2)}`;
    }
}



function buscarProductos(query) {
  fetch(`/buscar_productos/?q=${encodeURIComponent(query)}&tipo=${encodeURIComponent(tipoProducto)}`, {
    headers: {
      'X-Requested-With': 'XMLHttpRequest'
    }
  })
  .then(response => response.json())
  .then(data => {
    const contenedor = document.getElementById('productos-container');
    contenedor.innerHTML = '';
    data.productos.forEach(producto => {
        if (tipoProducto == 'farmacia') {
            contenedor.appendChild(crearCard(producto));
        } else {
            contenedor.appendChild(crearCardRopa(producto));
        }
      
    });
  })
  .catch(error => {
    console.error('Error al buscar productos:', error);
  });
}


function activarBoton(div) {
    const btnFarmacia = document.getElementById('btnFarmacia');
    const btnTienda = document.getElementById('btnTienda');

    btnFarmacia.classList.remove('bg-white', 'font-bold', 'text-black');
    btnTienda.classList.remove('bg-white', 'font-bold', 'text-black');

    div.classList.add('bg-white', 'font-bold', 'text-black');

}

function crearCard(producto) {
  const template = document.createElement('template');
  template.innerHTML = `
    <div class="flex flex-col justify-between rounded-lg shadow-sm">
        <div class="relative flex-1 object-contain bg-gray-300 rounded-lg rounded-b-none">
            <img src="${producto.imagen}" alt="${producto.nombre}" class="object-contain w-full h-32 rounded-lg rounded-b-none" />

            <!-- Ícono de ojo -->
            <button class="cursor-pointer ver-detalles absolute top-2 right-2 p-1 bg-opacity-90 rounded-full shadow"
                    data-nombre="${producto.nombre}" 
                    data-categoria="${producto.categoria || ''}" 
                    data-presentacion="${producto.presentacion || ''}"
                    data-concentracion="${producto.concentracion || ''}" 
                    data-descripcion="${producto.descripcion || 'Sin descripción'}"
                    data-imagen="${producto.imagen}">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" class="w-5 h-5" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                          d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                          d="M2.458 12C3.732 7.943 7.523 5 12 5s8.268 2.943 9.542 7c-1.274 4.057-5.065 7-9.542 7s-8.268-2.943-9.542-7z" />
                </svg>
            </button>
        </div>

        <div class="flex flex-col items-center justify-between p-2 bg-white border border-t-0 border-gray-300 rounded-lg rounded-t-none shadow-sm">
            <div class="w-full flex items-center justify-center">
                <h1 class="font-black text-xl">${producto.nombre}</h1>
            </div>
            <div class="flex flex-row w-full items-center justify-between mt-2">
                <div class="flex flex-col items-center justify-between">
                    <span class="font-black text-3xl text-green-600">C$ ${producto.precio}</span>
                    <p class="text-sm text-muted-foreground font-bold">Stock: ${producto.stock}</p>
                </div>
                <button class="cursor-pointer agregar-btn flex justify-center items-center text-gray-900 py-1 hover:bg-gray-200 p-4 hover:p-4 rounded-lg" data-id="${producto.id}" data-nombre="${producto.nombre}" data-precio="${producto.precio}" data-stock="${producto.stock}">
                    <svg fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5 flex mr-2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 0 0-16.536-1.84M7.5 14.25 5.106 5.272M6 20.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm12.75 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" />
                    </svg>
                    Agregar
                </button>
            </div>
        </div>
    </div>
  `.trim();

  return template.content.firstChild;
}

function crearCardRopa(producto) {
  const template = document.createElement('template');
  template.innerHTML = `
    <div class="flex flex-col justify-between rounded-lg shadow-sm">
        <div class="relative flex-1 object-contain bg-gray-300 rounded-lg rounded-b-none">
            <img src="${producto.imagen}" alt="${producto.nombre}" class="object-contain w-full h-32 rounded-lg rounded-b-none" />

            <!-- Ícono de ojo -->
            <button class="cursor-pointer ver-detalles absolute top-2 right-2 p-1 bg-opacity-90 rounded-full shadow"
                    data-nombre="${producto.nombre}" 
                    data-categoria="${producto.categoria || ''}" 
                    data-talla="${producto.talla || ''}"
                    data-descripcion="${producto.descripcion || ''}"
                    data-imagen="${producto.imagen}">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" class="w-5 h-5" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                          d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                          d="M2.458 12C3.732 7.943 7.523 5 12 5s8.268 2.943 9.542 7c-1.274 4.057-5.065 7-9.542 7s-8.268-2.943-9.542-7z" />
                </svg>
            </button>
        </div>

        <div class="flex flex-col items-center justify-between p-2 bg-white border border-t-0 border-gray-300 rounded-lg rounded-t-none shadow-sm">
            <div class="w-full flex items-center justify-center">
                <h1 class="font-black text-xl">${producto.nombre}</h1>
            </div>
            <div class="flex flex-row w-full items-center justify-between mt-2">
                <div class="flex flex-col items-center justify-between">
                    <span class="font-black text-3xl text-green-600">C$ ${producto.precio}</span>
                    <p class="text-sm text-muted-foreground font-bold">Talla: ${producto.talla}</p>
                </div>
                <button class="cursor-pointer agregar-btn flex justify-center items-center text-gray-900 py-1 hover:bg-gray-200 p-4 hover:p-4 rounded-lg" data-id="${producto.id}" data-nombre="${producto.nombre}" data-precio="${producto.precio}" data-stock="${producto.stock}">
                    <svg fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5 flex mr-2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 0 0-16.536-1.84M7.5 14.25 5.106 5.272M6 20.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm12.75 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" />
                    </svg>
                    Agregar
                </button>
            </div>
        </div>
    </div>
  `.trim();

  return template.content.firstChild;
}


function handleTipoPago() {
    const tipo = document.getElementById('tipo').value;
    const efectivo = document.getElementById('efectivo');
    const container = document.getElementById('extra-efectivo');

    // Limpiar el input mixto si existe
    container.innerHTML = '';

    if (tipo == '1') {
        efectivo.placeholder = 'Cordobas';
        efectivo.style.display = 'block';
    } else if (tipo == '2') {
        efectivo.placeholder = 'Dolares';
        efectivo.style.display = 'block';
    } else if (tipo == '3') {
        efectivo.placeholder = 'Cordobas';
        efectivo.style.display = 'block';

        const nuevoInput = document.createElement('input');
        nuevoInput.type = 'text';
        nuevoInput.id = 'efectivo-mixto';
        nuevoInput.placeholder = 'Dolares';
        nuevoInput.className = 'p-2 dark:bg-secondary-900 bg-gray-300 outline-none rounded-lg w-48 mr-1';
        container.appendChild(nuevoInput);
    } else if (tipo == '4') {
        efectivo.style.display = 'none';
        efectivo.value = '';
    }
}