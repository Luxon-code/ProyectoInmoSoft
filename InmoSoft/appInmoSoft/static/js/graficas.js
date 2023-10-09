const barras = document.getElementById('barras');
const botones = document.querySelectorAll('button');

// Función para generar colores aleatorios
function generarColoresAleatorios(numeroColores) {
  const colores = [];
  for (let i = 0; i < numeroColores; i++) {
    const color = `rgb(${Math.floor(Math.random() * 256)}, ${Math.floor(
      Math.random() * 256
    )}, ${Math.floor(Math.random() * 256)})`;
    colores.push(color);
  }
  return colores;
}

botones.forEach((button) => {
  button.addEventListener('click', (event) => {
    const filtro = event.target.getAttribute('data-filtro');
    let fechaActual = new Date();
    let fechaLimite;

    // Establecer la fecha límite en función del filtro seleccionado
    switch (filtro) {
      case 'Mensual':
        fechaLimite = new Date(fechaActual);
        fechaLimite.setMonth(fechaLimite.getMonth() - 1);
        break;
      case 'Trimestral':
        fechaLimite = new Date(fechaActual);
        fechaLimite.setMonth(fechaLimite.getMonth() - 3);
        break;
      case 'Semestral':
        fechaLimite = new Date(fechaActual);
        fechaLimite.setMonth(fechaLimite.getMonth() - 6);
        break;
      case 'Anual':
        fechaLimite = new Date(fechaActual);
        fechaLimite.setFullYear(fechaLimite.getFullYear() - 1);
        break;
      case 'Historico':
        fechaLimite = new Date(0); // Fecha mínima (histórico)
        break;
      default:
        fechaLimite = new Date(0); // Fecha mínima (histórico)
    }

    let url = `/numeroVentasPorAsesor/${filtro}`;

    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        const numeroVentasPorAsesor = data.numeroVentasPorAsesor;

        // Extraer las etiquetas y los datos de ventas del resultado
        const labels = numeroVentasPorAsesor.map((item) => item.username);
        const dataVentas = numeroVentasPorAsesor.map((item) => item.numeroVenta);

        // Generar colores aleatorios para las barras
        const coloresAleatorios = generarColoresAleatorios(labels.length);

        // Destruir la gráfica anterior si existe
        if (window.myChart) {
          window.myChart.destroy();
        }

        // Crear y actualizar la gráfica de barras con colores aleatorios
        window.myChart = new Chart(barras, {
          type: 'bar',
          data: {
            labels: labels,
            datasets: [
              {
                label: 'Numero De ventas',
                data: dataVentas,
                backgroundColor: coloresAleatorios,
                borderWidth: 1,
              },
            ],
          },
          options: {
            scales: {
              y: {
                beginAtZero: true,
              },
            },
          },
        });
      })
      .catch((error) => {
        console.error('Error al obtener los datos de ventas:', error);
      });
  });
});

document.addEventListener('DOMContentLoaded', function () {
  // Simular un clic en el botón "Histórico" al cargar la página
  const botonHistorico = document.querySelector('button[data-filtro="Historico"]');
  botonHistorico.click();
});


fetch('/ventas-por-mes/')
  .then(response => response.json())
  .then(data => {
    const colores = [
      'rgb(255, 99, 132)',
      'rgb(54, 162, 235)',
      'rgb(255, 205, 86)',
      'rgb(75, 192, 192)',
      'rgb(153, 102, 255)',
      'rgb(255, 159, 64)',
      'rgb(255, 0, 0)',      // Cambia estos colores según tus preferencias
      'rgb(0, 128, 0)',      // Cambia estos colores según tus preferencias
      'rgb(0, 0, 128)',      // Cambia estos colores según tus preferencias
      'rgb(128, 128, 0)',    // Cambia estos colores según tus preferencias
      'rgb(128, 0, 128)',    // Cambia estos colores según tus preferencias
      'rgb(0, 128, 128)'     // Cambia estos colores según tus preferencias
    ];

    const circular = document.getElementById('circular');
    new Chart(circular, {
      type: 'doughnut',
      data: {
        labels: data.labels,
        datasets: [{
          label: 'Ventas por Mes',
          data: data.data,
          backgroundColor: colores.slice(0, data.labels.length), // Tomar colores según la cantidad de meses
          hoverOffset: 4
        }]
      },
    });
  });
