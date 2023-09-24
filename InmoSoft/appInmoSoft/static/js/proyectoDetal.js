function readCarrusel(id){
    let url = `/proyectoDetalleCarrusel/${id}`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            const fotosInmueble = document.getElementById('fotosInmueble')
            const indicadores = document.getElementById('indicadores')
            let fotosInmuebles = ''
            let indicadoresHTML = ''
            data.imagenes.forEach((imagen,index) => {
                const inmuebleHtml = `<div class="carousel-item ${index==0?'active':''}" data-bs-interval="3000">
                <img src="/media/${imagen.imagen}" class="d-block" style="width: 100%; height: 15rem;" >
              </div>`;
                const indicadorHTML = `<button type="button" data-bs-target="#carouselExampleDark" data-bs-slide-to="${index}" class=${index==0 ?"active":""} ${index==0?'aria-current="true"':null} aria-label="Slide ${index+1}"></button>`
                indicadoresHTML += indicadorHTML
                fotosInmuebles += inmuebleHtml;
            });
            indicadores.innerHTML = indicadoresHTML;
            fotosInmueble.innerHTML = fotosInmuebles;
        })
        .catch(error => console.error('Error fetching data:', error));
}
