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
                                    <img src="${imageUrl}" class="card-img-top" alt="...">
                                </div>
                                <div class="card-body">
                                    <h5 class="card-title">${proyecto.nombre}</h5>
                                    <p class="card-text text-secondary">${proyecto.ubicacion}</p>
                                    <p class="text-secondary">${proyecto.descripcion}</p>
                                    <div class="border-bottom border-black"></div>
                                    <p class="text-secondary fw-bold">$ ${proyecto.precio}</p>
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
            let proyectosHmtl = ''
            data.proyectos.forEach(proyecto => {
                const imageUrl = `/media/${proyecto.foto}`;
                const proyectoHTML = `<div class="carousel-item active" data-bs-interval="10000">
                <img src="${imageUrl}" class="d-block" style="width: 100%; height: 25rem;" >
                <div class="carousel-caption d-none d-md-block">
                  <h5>${proyecto.nombre}</h5>
                  <p>${proyecto.ubicacion}</p>
                </div>
              </div>`;
                proyectosHmtl += proyectoHTML;
            });
            carruselProyectos.innerHTML = proyectosHmtl;
        })
        .catch(error => console.error('Error fetching data:', error));
}
readCarrusel();
readProyectos();
