async function guardarFactura() {
    const filas = document.querySelectorAll("#tabla-factura tbody tr");
    const productos = [];
    let hayError = false;
    let stockError = false;

    let tasaCambio = 0;

    // Esperar la tasa de cambio antes de continuar
    try {
        const response = await fetch('/api/tasa-cambio/');
        const data = await response.json();
        if (data.tasaCambio !== null && data.tasaCambio !== undefined) {
            tasaCambio = data.tasaCambio;
            console.log('Tasa de cambio actual:', tasaCambio);
        } else {
            console.error('No se encontró una tasa de cambio válida.');
            Swal.fire({ icon: 'error', title: 'No se encontró la tasa de cambio' });
            return;
        }
    } catch (error) {
        console.error('Error al obtener la tasa de cambio:', error);
        Swal.fire({ icon: 'error', title: 'Error al obtener la tasa de cambio' });
        return;
    }

    filas.forEach(fila => {
        const tipo = fila.getAttribute("data-tipo");
        const cantidad = parseInt(fila.querySelector(".cantidad").value);
        const precio = parseFloat(fila.querySelector(".precio").value);

        if (tipo === 'farmacia') {
            const stock = parseInt(fila.getAttribute("data-stock")) || 0;
            if (cantidad > stock) {
                stockError = true;
                return;
            }
        }

        if (isNaN(cantidad) || cantidad <= 0 || isNaN(precio) || precio <= 0) {
            hayError = true;
            return;
        }

        productos.push({
            id: parseInt(fila.getAttribute("data-id")),
            nombre: fila.getAttribute("data-nombre"),
            cantidad: cantidad,
            precio: precio,
            tipo: tipo
        });
    });

    if (stockError) {
        Swal.fire({ icon: 'warning', title: 'Stock insuficiente' });
        return;
    }

    if (productos.length === 0) {
        Swal.fire({ icon: 'warning', title: 'Agregue productos a la factura' });
        return;
    }

    if (hayError) {
        Swal.fire({ icon: 'warning', title: 'Datos inválidos en los productos' });
        return;
    }

    const totalTexto = document.getElementById("total-final").textContent.trim();
    const total = parseFloat(totalTexto.replace("C$", "").replace(",", ""));

    let cliente = document.getElementById("nombre-cliente").value.trim();
    if (!cliente) cliente = "Generico";

    const tipoPago = document.getElementById("tipo").value;
    let efectivoCordoba = 0;
    let efectivoDolar = 0;
    let cambio = 0;

    if (tipoPago === "1") {
        efectivoCordoba = parseFloat(document.getElementById("efectivo").value.trim()) || 0;
        if (efectivoCordoba == 0) {
            efectivoCordoba = total;
            cambio = 0;
        } else {
            if (efectivoCordoba < total) {
                Swal.fire({ icon: 'error', title: 'Monto insuficiente en córdobas' });
                return;
            }
            cambio = efectivoCordoba - total;
        }
    } else if (tipoPago === "2") {
        efectivoDolar = parseFloat(document.getElementById("efectivo").value.trim()) || 0;
        const totalEnCordobas = efectivoDolar * tasaCambio;
        if (efectivoDolar === 0 || totalEnCordobas < total) {
            Swal.fire({ icon: 'error', title: 'Monto insuficiente en dólares' });
            return;
        }
        cambio = totalEnCordobas - total;
    } else if (tipoPago === "3") {
        efectivoCordoba = parseFloat(document.getElementById("efectivo").value.trim()) || 0;
        efectivoDolar = parseFloat(document.getElementById("efectivo-mixto").value.trim()) || 0;
        const totalEnCordobas = efectivoCordoba + (efectivoDolar * tasaCambio);
        if (efectivoCordoba === 0 || efectivoDolar === 0 || totalEnCordobas < total) {
            Swal.fire({ icon: 'error', title: 'Monto insuficiente en efectivo mixto' });
            return;
        }
        cambio = totalEnCordobas - total;
    }

    const datos = {
        productos,
        total,
        cliente,
        tipo_pago: tipoPago,
        efectivo_cordoba: efectivoCordoba,
        efectivo_dolar: efectivoDolar,
    };

    fetch('/guardar-factura/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify(datos)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            Swal.fire({
                icon: 'success',
                title: 'Factura guardada correctamente',
                text: `Cambio: C$ ${cambio.toFixed(2)}`
            }).then(() => {
                window.location.reload();
            });
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Error al guardar',
                text: data.message || 'Hubo un problema al guardar la factura.'
            });
        }
    });
}
