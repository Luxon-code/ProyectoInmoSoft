function readVentasSeparadas(){
    let url = `/listarVentasSeparadas/`
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
                        <a><i class="bi bi-pencil"></i></a>
                     </td>
                 </tr>`;
         });
         tablaSeparados.innerHTML = table;
         cargarDataTable($("#tablaInmosoft"), "Inmuebles Separados", 4);
    });
}
function readVentasVendidas(){
    let url = `/listarVentasVendidas/`
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
                        <a><i class="bi bi-pencil"></i></a>
                     </td>
                 </tr>`;
         });
         tablaVendidos.innerHTML = table;
         cargarDataTable($("#tablaInmosoft"), "Inmubles Vendidos", 4);
    });
}
