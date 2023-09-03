function readInmuebles(id) {
    let url = `/listarInmuebles/${id}`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log(data)
            let table = ""
            data.inmuebles.forEach((element,index)=> {
                table+= `<tr class="text-center">
                <th scope="row">${index+1}</th>
                <td>$ ${element.Precio} COP</td>
                <td>${element.tipo}</td>
                <td>${element.disponibilidad}</td>
                <td><a href="" class="btn btn-secondary">Apartar</a></td>
            </tr>`
        });
        tblInmuebles.innerHTML = table
        cargarDataTable($("#tablaInmosoft"),"Inmuebles Disponibles",4);
        })
        .catch(error => console.error('Error fetching data:', error));
}
