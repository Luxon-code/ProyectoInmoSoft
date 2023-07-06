function readUsuarios(){
    let url = `/getUsuarios/`
    fetch(url)
    .then(response => response.json())
    .then(data => {
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
                <label class="form-check-label" for="switch${element.userCedula}">${element.is_active==true?'Activo':'Inactivo'}</label>
                </div>
            </td>
            <td><i class="bi bi-pencil-square fs-3"></i></td>
        </tr>`
        });
        tblUsers.innerHTML = table
        cargarDataTable($("#tablaInmosoft"),"Usuarios del sistema",5);
    })
}
function cambiarEstadoUsuario(id){
    let url = `/cambiarEstadoUsuario/${id}`
    fetch(url)
    .then(response =>response.json())
    .then(data =>{
        if(data.estado){
            location.reload()
        }
    })
}
readUsuarios()