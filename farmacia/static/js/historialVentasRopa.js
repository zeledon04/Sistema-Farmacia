
let rangoInicio = "";
let rangoFin = "";

document.getElementById("filtroFecha").addEventListener("change", function () {
    const fecha = this.value;
    const nombre = document.getElementById("filtroNombre").value;

    if (!fecha && !nombre) {
        window.location.href = '/Productos/historialVentasRopa'
    }


    if (fecha === "rango") {
        Swal.fire({
            title: 'Seleccionar Rango de Fechas',
            html: `
                <h3>Fecha Inicio</h3>'
                <input type="date" id="fechaInicio" class="swal2-input" placeholder="Desde">
                <h3 style="margin-top: 20px;">Fecha Fin</h3>
                <input type="date" id="fechaFin" class="swal2-input" placeholder="Hasta">
            `,
            confirmButtonText: 'Filtrar',
            focusConfirm: false,
            preConfirm: () => {
                const inicio = document.getElementById('fechaInicio').value;
                const fin = document.getElementById('fechaFin').value;
                if (!inicio || !fin) {
                    Swal.showValidationMessage("Ambas fechas son requeridas");
                    return false;
                }
                return { inicio, fin };
            }
        }).then((result) => {
            if (result.isConfirmed) {
                rangoInicio = result.value.inicio;
                rangoFin = result.value.fin;
                filtrar(nombre, fecha, rangoInicio, rangoFin);
            } else {
                // Si cancela, restablecemos el select
                document.getElementById("filtroFecha").value = "";
            }
        });
    } else {
        // Reiniciamos valores de rango si no se elige "rango"
        rangoInicio = "";
        rangoFin = "";
        filtrar(nombre, fecha);
    }
});

document.getElementById("filtroNombre").addEventListener("input", function () {
    const nombre = this.value;
    const fecha = document.getElementById("filtroFecha").value;

    if (!nombre && !fecha) {
        window.location.href = '/Productos/historialVentasRopa'
    }

    filtrar(nombre, fecha, rangoInicio, rangoFin);
});

function filtrar(nombre, fecha, inicio = "", fin = "") {
    const url = `/filtrar-ventas/?nombre=${encodeURIComponent(nombre)}&fecha=${fecha}&inicio=${inicio}&fin=${fin}&tipo=tienda`;
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector("#datos tbody");
            tbody.innerHTML = "";
            data.ventas.forEach(venta => {
                const fila = `
                    <tr class="main-row hover:bg-gray-200 rounded-lg transition-colors main-row">
                        <td class="p-3 text-2xl text-center">${venta.cont}</td>
                        <td class="p-3 text-2xl text-center">${venta.producto}</td>
                        <td class="p-3 text-2xl text-center">${venta.fecha}</td>
                        <td class="p-3 text-2xl text-center">${venta.cantidad}</td>
                        <td class="p-3 text-2xl text-center">${formatCurrency(venta.precio)}</td>
                        <td class="p-3 text-2xl text-center">${formatCurrency(venta.precio * venta.cantidad)}</td>
                    </tr>
                `;
                tbody.innerHTML += fila;
            });
        });
}



function formatCurrency(value) {
    return `C$ ${parseFloat(value).toFixed(2)}`;
}
