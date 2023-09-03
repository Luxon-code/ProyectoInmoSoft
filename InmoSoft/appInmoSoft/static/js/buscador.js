window.onload = () => {
    searchPokemon()
}
function autoComplet(){
    fetch("/listarProyectos/")
        .then(response => response.json())
        .then(data => {
            let textoBuscar = document.getElementById("inputbuscar").value
            if(textoBuscar.length >=2){
                let lista = `<div class="list-group">`
                const filtroPokemon = data.proyectos.filter(filtrar)
                filtroPokemon.forEach(element => {
                    lista += `<a href="/vistaDetalleProyecto/${element.id}" class="list-group-item list-group-item-action">${element.nombre} - ${element.ubicacion} <img src="/media/${element.foto}" alt="fotoProyecto" style="width:20px;height:20px;"/></a>`;
                });
                lista += `</div>`
                document.getElementById("listProyectos").innerHTML = lista
                document.getElementById("listProyectos").style  = `height: 380px;overflow: auto;`
            }else{
                document.getElementById("listProyectos").innerHTML = ""
            }
        })
}
function filtrar(element) {
    let textoBuscar = document.getElementById("inputbuscar").value.toLowerCase();
    let nombre = element.nombre.toLowerCase();
    let ubicacion = element.ubicacion.toLowerCase();
    
    // Ahora estamos comprobando si el texto de búsqueda se encuentra en el nombre o la ubicación.
    return nombre.includes(textoBuscar) || ubicacion.includes(textoBuscar);
}

function searchPokemon(){
    document.getElementById("inputbuscar").addEventListener("search", (event) =>{
        document.getElementById("listProyectos").innerHTML = ""
        document.getElementById("listProyectos").style = "overflow:hidden;"
        document.getElementById("inputbuscar").value = ""
    })
}