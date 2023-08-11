function readProyectos() {
    let url = `/getProyecto/`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const listaInmuebles = document.getElementById('ListaInmuebles'); // Obtén el elemento contenedor
            let projectsHTML = ''; // Variable para almacenar el HTML de las tarjetas de proyectos

            data.proyectos.forEach(proyecto => {
                const imageUrl = `/media/${proyecto.proFoto}`; // Construye la URL completa de la imagen
                const projectHTML = `
                    <div class="col-sm d-flex justify-content-center">
                        <a href="" style="text-decoration: none;">
                            <div class="card my-3 cardProyecto" style="width: 20rem;">
                                <div class="card-header text-center bg-danger text-white text-uppercase">
                                    ${proyecto.proNombre}
                                </div>
                                <div class="bg-danger">
                                    <img src="${imageUrl}" class="card-img-top" alt="...">
                                </div>
                                <div class="card-body">
                                    <h5 class="card-title">${proyecto.proNombre}</h5>
                                    <p class="card-text text-secondary">${proyecto.proUbicacion_id}</p>
                                    <p class="text-secondary">${proyecto.proDescripcion}</p>
                                    <div class="border-bottom border-black"></div>
                                    <p class="text-secondary fw-bold">$${proyecto.proTotalInmuebles}</p>
                                </div>
                            </div>
                        </a>
                    </div>
                `;
                projectsHTML += projectHTML;
            });

            // Agregar el HTML de las tarjetas de proyectos al contenedor
            listaInmuebles.innerHTML = projectsHTML;
        })
        .catch(error => console.error('Error fetching data:', error));
}

readProyectos();
