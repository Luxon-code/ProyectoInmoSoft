function readProyectos() {
    let url = `/listarProyectos/`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const listaProyectos = document.getElementById('listaProyectos'); // Obtén el elemento contenedor
            let projectsHTML = ''; // Variable para almacenar el HTML de las tarjetas de proyectos
            console.log(data);
            data.proyectos.forEach(proyecto => {
                const imageUrl = `/media/${proyecto.foto}`; // Construye la URL completa de la imagen
                const projectHTML = `
                    <div class="col-sm d-flex justify-content-center">
                        <a href="/vistaDetalleInmueble/${proyecto.id}" style="text-decoration: none;">
                            <div class="card my-3 cardProyecto" style="width: 20rem;">
                                <div class="card-header text-center bg-danger text-white text-uppercase">
                                    Nuevo Proyecto
                                </div>
                                <div class="bg-danger">
                                    <img src="${imageUrl}" class="card-img-top" style=height:11rem;>
                                </div>
                                <div class="card-body">
                                    <h5 class="card-title">${proyecto.nombre}</h5>
                                    <p class="card-text text-secondary">Ubicacion: ${proyecto.ubicacion}</p>
                                    <p class="text-secondary">${limitarLongitud(proyecto.descripcion,100)}</p>
                                    <div class="border-bottom border-black"></div>
                                    <p class="text-secondary fw-bold">Desde: $ ${proyecto.precio}</p>
                                </div>
                            </div>
                        </a>
                    </div>
                `;
                projectsHTML += projectHTML;
            });

            // Agregar el HTML de las tarjetas de proyectos al contenedor
            listaProyectos.innerHTML = projectsHTML;
        })
        .catch(error => console.error('Error fetching data:', error));
}

function readCarrusel(){
    let url = `/proyectosCarrusel/`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            const carruselProyectos = document.getElementById('CarruselProyectos')
            const indicadores = document.getElementById('indicadores')
            let proyectosHmtl = ''
            let indicadoresHTML = ''
            data.proyectos.forEach((proyecto, index) => {
                const imageUrl = `/media/${proyecto.foto}`;
                const proyectoHTML = `<div class="carousel-item ${index==0?'active':''}" data-bs-interval="10000">
                <img src="${imageUrl}" class="d-block" style="width: 100%; height: 25rem;" >
                <div class="carousel-caption d-none d-md-block">
                  <h5>${proyecto.nombre}</h5>
                  <p>${proyecto.ubicacion}</p>
                </div>
              </div>`;
                const indicadorHTML = `<button type="button" data-bs-target="#carouselExampleDark" data-bs-slide-to="${index}" class=${index==0 ?"active":""} ${index==0?'aria-current="true"':null} aria-label="Slide ${index+1}"></button>`
                indicadoresHTML += indicadorHTML
                proyectosHmtl += proyectoHTML;
            });
            indicadores.innerHTML = indicadoresHTML;
            carruselProyectos.innerHTML = proyectosHmtl;
        })
        .catch(error => console.error('Error fetching data:', error));
}
function limitarLongitud(cadena, longitudMaxima) {
    if (cadena.length > longitudMaxima) {
      return cadena.slice(0, longitudMaxima) + "...";
    }
    return cadena;
  }
readCarrusel();
readProyectos();
