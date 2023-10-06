function readListaMora(){
    let url = `/ObtenerListaMora/`
    tablaMora.innerHTML = `<tr>
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
         data.ListaMora.forEach((Mora) => {
             table += `
             
                 <tr class="text-center">
                     <td>${Mora.id}</td>
                     <td>${Mora.numCuotaActual}</td>
                     <td>${Mora.cliente}</td>
                     <td>${Mora.estado}</td>
                     <td>
                     <a href="/actualizarPago/${Mora.idRegistroPago}" class="btn btn-outline-secondary btn-sm"><i class="fa-solid fa-file-invoice-dollar fa-fade"></i> Pago</a> 
                     </td>
                 </tr>`;
         });
         tablaMora.innerHTML = table;
         cargarDataTable($("#tablaInmosoft"), "Inmuebles Separados", 5);
       
    });
}