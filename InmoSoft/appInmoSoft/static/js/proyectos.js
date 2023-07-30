const departamentoSelect = document.getElementById("cbDepartamento");
const municipioSelect = document.getElementById("cbMunicipio");
const departamentos = []
// Función para cargar los departamentos en el primer campo "select".
function cargarDepartamentos() {
    let url = `https://www.datos.gov.co/resource/xdk5-pm3f.json?$query=SELECT%20%60departamento%60%2C%20count(*)%20AS%20%60count%60%20GROUP%20BY%20%60departamento%60`
    fetch(url)
    .then(response =>response.json())
    .then(data =>{
        data.forEach((item) => {
            const option = document.createElement("option");
            option.text = item.departamento;
            option.value = item.departamento;
            departamentos.push(item.departamento);
            departamentoSelect.add(option);
        });
    })
}
// Función para cargar los municipios en el segundo campo "select" al seleccionar un departamento.
function actualizarMunicipios() {
    const departamentoSeleccionado = departamentoSelect.value;
    municipioSelect.innerHTML = '<option value="">Selecciona un municipio</option>'; // Reiniciar la lista de municipios.
  
    if (departamentoSeleccionado) {
      const departamentoExiste = departamentos.find((departamento) => departamento === departamentoSeleccionado);
      if (departamentoExiste) {
        let url = `https://www.datos.gov.co/resource/xdk5-pm3f.json?$query=SELECT%20%60municipio%60%20WHERE%20%60departamento%60%20IN%20("${departamentoSeleccionado}")`
        fetch(url)
        .then(response =>response.json())
        .then(data =>{
            data.forEach((item) => {
                const option = document.createElement("option");
                option.text = item.municipio;
                option.value = item.municipio;
                municipioSelect.add(option);
            });
        })
      }
    }
  }
cargarDepartamentos()


    // Función para guardar los datos del primer formulario en el almacenamiento local
function guardarDatosPrimerFormulario() {
    const formulario = document.getElementById('formularioDatos1');
    const formData = new FormData(formulario);
  
    // Convertir la imagen a un objeto Blob
    const imagenInput = formulario.querySelector('input[type="file"]');
    const imagenBlob = imagenInput.files[0];
  
    // Crear un objeto con los datos del formulario y la imagen Blob
    const datos = {
      nombreProyecto: formData.get('txtNombreProyecto'),
      fiducia: formData.get('cbFiducia'),
      numeroTorresOManzanas: formData.get('txtNumeroTorresoManzanas'),
      numeroApartamentosOCasas: formData.get('txtNumerosApartamentosoCasas'),
      totalInmuebles: formData.get('txtTotalInmuebles'),
      obraEntregable: formData.get('cbObraentregable'),
      parqueadero: formData.get('cbParqueadero'),
      departamento: formData.get('cbDepartamento'),
      ciudad: formData.get('cbMunicipio'),
      direccion: formData.get('txtDireccion'),
      descripcion: formData.get('txtDescripcion'),
    };
    // Crear una URL de objeto para representar la imagen
    const imagenUrl = URL.createObjectURL(imagenBlob);
    datos.imagen = imagenUrl;
  
    // Guardar el objeto de datos en localStorage
    localStorage.setItem('datosFormulario', JSON.stringify(datos));
  
    console.log('Datos del primer formulario guardados en localStorage:', datos);
}
  
  

  