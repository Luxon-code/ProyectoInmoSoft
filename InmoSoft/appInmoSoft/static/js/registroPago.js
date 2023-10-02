function readVentasVendidas(){
    let url = `/listarVentasVendidas/`
    tablaVendidos.innerHTML = `<tr>
    <td colspan="5" class="text-center">
        <div class="row d-flex justify-content-center">
        <div class="custom-loader"></div>
        </div>
    </td>
    </tr>`
    fetch(url)
    .then(response => response.json())
    .then(data => {
        console.log(data)
         let table = ""
         data.ventas.forEach((venta) => {
             table += `
                 <tr class="text-center">
                     <td>${venta.id}</td>
                     <td>${venta.cliente}</td>
                     <td>${venta.proyecto}</td>
                     <td>${venta.estado}</td>
                     <td>
                        <a onclick="abrirModal(${venta.idVen})" style="text-decoration: none; color: #6B85B3"><i class="fa fa-duotone fa-file-circle-plus fa-fade fa-lg"></i></a> 
                     </td>
                 </tr>`;
         });
         tablaVendidos.innerHTML = table;
         cargarDataTable($("#tablaInmosoft"), "Inmubles Vendidos", 4);
    });
}


 // Obtener la fecha actual
 var fechaActual = new Date();

 // Obtener el elemento de entrada de fecha
 var txtFechaInicial = document.getElementById("txtFechaInicial");

 // Obtener el elemento de entrada de mes
 var txtMes = document.getElementById("txtMes");

 // Formatear la fecha en formato YY/MM/DD
 var formatoFecha = fechaActual.getFullYear() + "/" + (fechaActual.getMonth() + 1).toString().padStart(2, '0') + "/" + fechaActual.getDate().toString().padStart(2, '0');

 // Obtener el nombre del mes
 var nombreMes = obtenerNombreMes(fechaActual.getMonth());

 // Establecer el valor de los elementos de entrada
 txtFechaInicial.value = formatoFecha;
 txtMes.value = nombreMes;

 // Función para obtener el nombre del mes
 function obtenerNombreMes(mes) {
     var meses = [
         "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
         "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
     ];
     return meses[mes];
 }

