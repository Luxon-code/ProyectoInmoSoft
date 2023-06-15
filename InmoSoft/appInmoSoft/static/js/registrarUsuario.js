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