function readInmuebles(id) {
    let url = `/listarInmuebles/${id}`;
    tblInmuebles.innerHTML = `<tr>
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
            data.inmuebles.forEach((element,index)=> {
                table+= `<tr class="text-center">
                <th scope="row">${element.id}</th>
                <td>$ ${element.Precio} COP</td>
                <td>${element.tipo}</td>
                <td>${element.disponibilidad}</td>
                <td><a href="/vistaSepararInmueble/${element.id}/" class="btn btn-secondary"><i class="fa fa-solid fa-building-user fa-flip"></i> Apartar</a></td>
            </tr>`
        });
        tblInmuebles.innerHTML = table
        cargarDataTable($("#tablaInmosoft"),"Inmuebles Disponibles",4);
        })
        .catch(error => console.error('Error fetching data:', error));
}
