

// Line chart -- Ingresos Mensuales en el último año (Gráfico Lineal)
fetch("api/ingresos_mensuales/")
    .then(response => response.json())
    .then(data => {
        const lctx = document.getElementById('lineChartIngresos').getContext("2d");
        // Crear el degradado vertical
        const gradient = lctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(54, 162, 235, 0.5)');   // Color en la parte superior
        gradient.addColorStop(1, 'rgba(255, 255, 255, 0)');     // Transparente abajo
        const lineChartIngresos = new Chart(lctx, {
            type: 'line',
            data: {
                labels: data.sales_labels,
                datasets: [{
                    label: 'Ingresos mensuales',
                    data: data.sales_data,
                    borderColor: 'rgb(54, 162, 235)',
                    backgroundColor: gradient,  // Aquí usamos el degradado
                    pointBackgroundColor: 'rgb(54, 162, 235)',  // color de los puntos
                    pointRadius: 4,
                    pointHoverRadius: 6, // Agrandaa el tamaño del punto al pasar el mouse(hover)
                    tension: 0.3,
                    fill: true,  // Esto activa que se vea el área rellena
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function (value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: '#333',
                            font: {
                                size: 14
                            }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                return `Ingresos: $${context.parsed.y.toLocaleString()}`;
                            }
                        }
                    }
                }
            }
        });

        // lineChartIngresos();
    })