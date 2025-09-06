
// Line chart -- Ventas Mensuales en el último año (Gráfico Lineal)
fetch("api/ventas_mensuales/")
    .then(response => response.json())
    .then(data => {
        const lctx = document.getElementById('lineChart').getContext("2d");
        const gradient = lctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(75, 192, 192, 0.5)'); // Celeste más fuerte arriba
        gradient.addColorStop(1, 'rgba(75, 192, 192, 0)');   // Transparente abajo
        const lineChart = new Chart(lctx, {
            type: 'line',
            data: {
                labels: data.sales_labels,
                datasets: [{
                    label: 'Cantidad de ventas',
                    data: data.sales_data,
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: gradient,
                    tension: 0.3,
                    fill: true,
                    pointBackgroundColor: 'rgb(75, 192, 192)',  // color de los puntos
                    pointRadius: 4,
                    pointHoverRadius: 6,
                }]
            }
        });

        // lineChart();
    })