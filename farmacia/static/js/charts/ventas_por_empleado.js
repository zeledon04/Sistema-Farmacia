

// Bar chart --> Ventas por Empleado (Gráfico de Barras)
fetch('/api/ventas_por_empleado/')
    .then(res => res.json())
    .then(data => {
        const bctx = document.getElementById('barChart').getContext("2d");

        // Generar colores aleatorios pero agradables
        const backgroundColors = data.labels.map(() => {
            const r = Math.floor(Math.random() * 100 + 100); // 100–200
            const g = Math.floor(Math.random() * 100 + 150); // 150–250
            const b = Math.floor(Math.random() * 100 + 200); // 200–300
            return `rgba(${r}, ${g}, ${b}, 0.6)`;
        });

        new Chart(bctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Ventas (Cantidad/Empleado)',
                    data: data.data,
                    backgroundColor: backgroundColors,
                    borderColor: 'rgb(75, 192, 192)',
                    borderWidth: 1
                }]
            },

        });
    });