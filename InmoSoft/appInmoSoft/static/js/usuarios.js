document.addEventListener('DOMContentLoaded', function() {
    function previewImage(event) {
        var input = event.target;
        var imgPerfil = document.querySelector('.imgPerfil img');

        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function(e) {
                imgPerfil.src = e.target.result;
            }

            reader.readAsDataURL(input.files[0]);
        } else {
            // Imagen por defecto en caso de no seleccionar ninguna
            imgPerfil.src = '../media/usuario-icono.png';
        }
    }

    var fileInput = document.getElementById('fileFoto');
    fileInput.addEventListener('change', previewImage);
});
function readUsuarios(){
    let url = `/getUsuarios/`
    fetch(url)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        let table = ""
        data.usuarios.forEach((element,index)=> {
            table+= `<tr class="text-center">
            <td>${element.userCedula}</td>
            <td>${element.first_name} ${element.last_name}</td>
            <td>${element.userTelefono}</td>
            <td>${element.userTipo}</td>
            <td>
                <div class="form-check form-switch">
                <input onclick="cambiarEstadoUsuario(${element.id})" class="form-check-input" type="checkbox" role="switch" id="switch${element.userCedula}" ${element.is_active==true?"checked":""}>
                <label class="form-check-label" for="switch${element.nombrePro}">${element.is_active==true?"Activo":"Inactivo"}</label>
                </div>
            </td>
            <td><i class="bi bi-pencil-square fs-3"></i></td>
        </tr>`
            localStorage.idSolicitud = element.idSolicitud
        });
        tblUsers.innerHTML = table
    })
}
function cambiarEstadoUsuario(id){
    let url = `/cambiarEstadoUsuario/${id}`
    fetch(url)
    .then(response =>response.json())
    .then(data =>{
        console.log(data)
        readUsuarios()
    })
}
readUsuarios()