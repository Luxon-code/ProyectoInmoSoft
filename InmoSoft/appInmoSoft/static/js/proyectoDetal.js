function readCarrusel(id){
    let url = `/proyectoDetalleCarrusel/${id}`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            const fotosInmueble = document.getElementById('fotosInmueble')
            let fotosInmuebles = ''
            data.imagenes.forEach((imagen,index) => {
                const inmuebleHtml = `<div class="carousel-item ${index==0?'active':''}" data-bs-interval="10000">
                <img src="/media/${imagen.imagen}" class="d-block" style="width: 100%; height: 15rem;" >
              </div>`;
                fotosInmuebles += inmuebleHtml;
            });
            fotosInmueble.innerHTML = fotosInmuebles;
        })
        .catch(error => console.error('Error fetching data:', error));
}
