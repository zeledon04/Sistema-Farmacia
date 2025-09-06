document.addEventListener("DOMContentLoaded", function () {

// Pie chart --> Estado del Inventario (Gráfico Circular)
fetch("/api/estado_inventario/")
    .then(res => res.json())
    .then(data => {
        const pctx = document.getElementById('pieChart').getContext("2d");

        new Chart(pctx, {
            type: 'pie',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.data,
                    backgroundColor: [
                        'rgba(75, 192, 192, 0.6)',  // En Stock (celeste)
                        'rgba(255, 206, 86, 0.6)',  // Bajo Stock (amarillo)
                        'rgba(255, 99, 132, 0.6)'   // Agotado (rojo)
                    ],
                    borderColor: [
                        'rgba(75, 192, 192, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(255, 99, 132, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    }
                }
            }
        });

    });
});