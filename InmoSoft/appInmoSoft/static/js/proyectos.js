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
      const formData = {
          nombreProyecto: document.getElementById('txtNombreProyecto').value,
          fiducia: document.getElementById('cbFiducia').value,
          numeroTorresOManzanas: document.getElementById('txtNumeroTorresoManzanas').value,
          numeroApartamentosOCasas: document.getElementById('txtNumerosApartamentosoCasas').value,
          totalInmuebles: document.getElementById('txtTotalInmuebles').value,
          obraEntregable: document.getElementById('cbObraentregable').value,
          parqueadero: document.getElementById('cbParqueadero').value,
          departamento: document.getElementById('cbDepartamento').value,
          ciudad: document.getElementById('cbMunicipio').value,
          direccion: document.getElementById('txtDireccion').value,
          descripcion: document.getElementById('txtDescripcion').value,
          // Agrega aquí los valores de otros campos del primer formulario que desees guardar
      };
      localStorage.setItem('primerFormularioData', JSON.stringify(formData));
  }

  // Función para cargar y rellenar el primer formulario con los datos guardados
  function cargarDatosPrimerFormulario() {
      const formData = JSON.parse(localStorage.getItem('primerFormularioData'));
      if (formData) {
          document.getElementById('txtNombreProyecto').value = formData.nombreProyecto;
          document.getElementById('cbFiducia').value = formData.fiducia;
          document.getElementById('txtNumeroTorresoManzanas').value = formData.numeroTorresOManzanas;
          document.getElementById('txtNumerosApartamentosoCasas').value = formData.numeroApartamentosOCasas;
          document.getElementById('txtTotalInmuebles').value = formData.totalInmuebles;
          document.getElementById('cbObraentregable').value = formData.obraEntregable;
          document.getElementById('cbParqueadero').value = formData.parqueadero;
          document.getElementById('cbDepartamento').value = formData.departamento;
          document.getElementById('cbMunicipio').value = formData.ciudad;
          document.getElementById('txtDireccion').value = formData.direccion;
          document.getElementById('txtDescripcion').value = formData.descripcion;
          // Rellena otros campos del primer formulario según sea necesario
      }
  }

  