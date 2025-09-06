const bctx = document.getElementById('barChart').getContext("2d");
const lctx = document.getElementById('lineChart').getContext("2d");
const pctx = document.getElementById('pieChart').getContext("2d");
const bIctx = document.getElementById('barIChart').getContext("2d");

// Bar chart --> Ventas por Categorías(Gráfico de Barras)
const categoryData = [45000, 28000, 35000, 18000, 12000]

const categoryLabels = ["Hidratantes", "Nutrición", "Cremas", "Medicamentos Controlados", "Otros"]

const barChart = new Chart(bctx, {
    type: 'bar',
    data: {
        labels: categoryLabels,
        datasets: [{
            label: 'Cantidad',
            data: categoryData,
            backgroundColor: [
                'rgba(255, 99, 132)',
                'rgba(255, 159, 64)',
                'rgba(255, 205, 86)',
                'rgba(75, 192, 192)',
                'rgba(54, 162, 235)',
                'rgba(153, 102, 255)',
                'rgba(201, 203, 207)'
            ]
        }]
    }
});

// Line chart -- Ventas Mensuales en el último año (Gráfico Lineal)
const salesData = [1200, 1800, 2200, 1500, 2500, 3000, 2800, 3200, 3800, 4000, 4500, 5000]
const salesLabels = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic",]

const lineChart = new Chart(lctx, {
    type: 'line',
    data: {
        // labels: ['Red', 'Blue', 'Yellow'],
        labels: salesLabels,
        datasets: [{
            label: 'Cantidad',
            // data: [65, 59, 80, 81, 56, 55, 40],
            data: salesData,
            // backgroundColor: ['red', 'blue', 'yellow'],
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }]
    }
});


// Pie chart -- Estado del Inventario (Gráfico de Pastel)
const inventoryStatusData = [65, 25, 10]
const inventoryStatusLabels = ["En stock", "Bajo stock", "Agotado"]

const pieChart = new Chart(pctx, {
    type: 'pie',
    data: {
        // labels: ['Red', 'Blue', 'Yellow'],
        labels: inventoryStatusLabels,
        datasets: [{
            label: 'Cantidad',
            // data: [65, 59, 80, 81, 56, 55, 40],
            data: inventoryStatusData,
            // backgroundColor: ['red', 'blue', 'yellow'],
            backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 205, 86)'
            ],
            tension: 0.1
        }]
    }
});

// Bar chart --> Distribución de Inventario, Cantidad de productos por categoría(Gráfico de Barras)
const inventoryData = [120, 80, 150, 70, 50]

const inventoryLabels = ["Hidratantes", "Nutrición", "Cremas", "Medicamentos Controlados", "Otros"]

const barIChart = new Chart(bIctx, {
    type: 'bar',
    data: {
        labels: inventoryLabels,
        datasets: [{
            label: 'Cantidad',
            data: inventoryData,
            backgroundColor: [
                'rgba(255, 99, 132, 0.7)',
                'rgba(255, 159, 64, 0.7)',
                'rgba(255, 205, 86, 0.7)',
                'rgba(75, 192, 192, 0.7)',
                'rgba(54, 162, 235, 0.7)',
                'rgba(153, 102, 255, 0.7)',
                'rgba(201, 203, 207, 0.7)'
            ]
        }]
    }
});

