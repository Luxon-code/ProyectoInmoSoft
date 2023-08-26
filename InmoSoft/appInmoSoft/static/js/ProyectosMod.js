function formatDate(dateString) {
    const options = { day: '2-digit', month: '2-digit', year: '2-digit' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

function readProyectos() {
    let url = `/listarProyectos/`
    fetch(url)
    .then(response => response.json())
    .then(data => {
        let table = ""
        data.proyectos.forEach((proyecto, index) => {
            const formattedDate = formatDate(proyecto.fecha);

            table += `
                <tr class="text-center">
                    <td>${proyecto.nombre}</td>
                    <td>${proyecto.fiducia}</td>
                    <td>${formattedDate}</td>
                    <td>${proyecto.totalinmuebles}</td>
                    <td>${proyecto.ubicacion}</td>
                    <td>
                        <button class="btn btn-info btn-sm" onclick="abrirModal(${proyecto.id})">
                            <i class="bi bi-pencil"></i> Editar
                        </button>
                    </td>
                </tr>`;
        });
        tblProyectos.innerHTML = table;
        cargarDataTable($("#tablaInmosoft"), "Proyectos del sistema", 6);
    });
}








function cambiarImagen(event) {
    const fileInput = event.target;
    const imgElement = document.querySelector('.imgPerfil2 img');

    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            imgElement.src = e.target.result; // Set the source of the image
        };
        reader.readAsDataURL(fileInput.files[0]);
    }
}



readProyectos();
