document.addEventListener('DOMContentLoaded', function() {
        document.getElementById('generar_reporte_factura').addEventListener('click', generarReporteFactura);
    });
    
    function generarReporteFactura(event) {
        event.preventDefault();
    
        var datos = [];
        var filas = document.querySelectorAll('#datos tbody tr.main-row');
    
        filas.forEach(function(fila) {
            if (fila.style.display !== 'none') {
                var celdas = fila.querySelectorAll('td');
                const limpiarMoneda = (texto) => texto.replace('C$', '').trim();

                
                let dato = {};

                if (celdas.length === 7) {
                    // Tabla con precio de compra (Farmacia)
                    dato = {
                        'numero': celdas[0].innerText,
                        'producto': celdas[1].innerText,
                        'fecha': celdas[2].innerText,
                        'precioCompra': limpiarMoneda(celdas[3].innerText),
                        'cantidad': celdas[4].innerText,
                        'precioVenta': limpiarMoneda(celdas[5].innerText),
                        'subtotal': limpiarMoneda(celdas[6].innerText),
                    };
                } else {
                    // Tabla sin precio de compra (Ropa)
                    dato = {
                        'numero': celdas[0].innerText,
                        'producto': celdas[1].innerText,
                        'fecha': celdas[2].innerText,
                        'cantidad': celdas[3].innerText,
                        'precioVenta': limpiarMoneda(celdas[4].innerText),
                        'subtotal': limpiarMoneda(celdas[5].innerText),
                    };
                }

                console.log(dato);
                datos.push(dato);
            }
        });
    
        var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        console.log(URL_IMPRIMIR_VENTAS);
    
        fetch(URL_IMPRIMIR_VENTAS, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ items: datos })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.open(URL_PDF_VENTAS, '_blank');
            } else {
                alert('Error al generar registro. Inténtalo de nuevo.');
            }
        })
        .catch(error => {
            console.error('Error al generar registro:', error);
        });
    }