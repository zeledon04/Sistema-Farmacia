document.addEventListener('DOMContentLoaded', function() {
        document.getElementById('generar_reporte_inventario').addEventListener('click', generarReporteInventario);
    });

function generarReporteInventario(event) {
    event.preventDefault();

    var filas = document.querySelectorAll('#datos tbody tr.main-row');
    let primeraFecha = null;

    for (let fila of filas) {
        if (fila.style.display !== 'none') {
            let celdas = fila.querySelectorAll('td');
            primeraFecha = celdas[2].innerText;
            console.log(primeraFecha);
            break;
        }
    }

    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/inventario/pdf/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ fecha: primeraFecha })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.open('/registroInventario/pdf/', '_blank');
        } else {
            alert('Error al generar registro. Inténtalo de nuevo.');
        }
    })
    .catch(error => {
        console.error('Error al generar registro:', error);
    });
}