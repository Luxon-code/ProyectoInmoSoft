// Obtén el valor de la cuota inicial y el número de cuotas ingresados por el usuari
const numCuotasInput = document.getElementById("txtNumeroCuotas");
const resultadoTabla = document.getElementById("tablaPlan");

// Agrega un event listener para calcular el plan de pago cuando se haga clic en el botón "Calcular Plan"
document.getElementById("btnCalcularPlan").addEventListener("click", function() {
    if(numCuotasInput.value!=""){
        const numCuotas = parseInt(numCuotasInput.value);
        // Obtenemos el valor del inmueble desde el elemento HTML
        var valorInmueble = parseFloat(document.getElementById('precioInmuble').value);
        var valorSeparacion = parseFloat(document.getElementById('costoSeparacion').value);
    
        // Calculamos el 30% del valor del inmueble
        var cuotaInicial = Math.round(valorInmueble * 0.3);
        // Calcula el valor de cada cuota mensual
        const valorPorCuota = Math.round((cuotaInicial - valorSeparacion) / numCuotas);

        document.getElementById("cuotaInicial").value=cuotaInicial;
        valorCuota.value=valorPorCuota;
    
        // Limpia la tabla existente
        resultadoTabla.innerHTML = "";
    
        // Calcula la fecha de inicio del plan de pago
        const fechaInicio = new Date(); // Puedes ajustar esto según tu lógica
        const diaInicio = fechaInicio.getDate();
        const mesInicio = fechaInicio.getMonth() + 1; // Suma 1 porque los meses son 0-indexados
        const añoInicio = fechaInicio.getFullYear();
    
        // Calcula la fecha de finalización del plan de pago
        const fechaFinal = new Date();
        fechaFinal.setMonth(fechaFinal.getMonth() + numCuotas-1); // Ajusta según la duración del plan
        const diaFinal = fechaFinal.getDate();
        const mesFinal = fechaFinal.getMonth()+1 ; // Suma 1 porque los meses son 0-indexados
        const añoFinal = fechaFinal.getFullYear();
    
        // Asigna los valores de las fechas de inicio y finalización a los campos ocultos
        document.getElementById("fechaInicio").value = `${diaInicio}/${mesInicio}/${añoInicio}`;
        document.getElementById("fechaFinal").value = `${diaFinal}/${mesFinal}/${añoFinal}`;
    
        // Llena la tabla con los detalles del plan de pago
        for (let i = 0; i < numCuotas; i++) {
            const fecha = new Date(); // Puedes calcular las fechas según tu lógica
            fecha.setMonth(fecha.getMonth() + i);
    
            const newRow = resultadoTabla.insertRow();
            const fechaCell = newRow.insertCell(0);
            const planPagoCell = newRow.insertCell(1);
            const mesesCell = newRow.insertCell(2);
            const cuotaCell = newRow.insertCell(3);
    
            // Obtén el día, el mes y el año de la fecha
            const dia = fecha.getDate();
            const mes = fecha.getMonth() + 1; // Suma 1 ya que los meses en JavaScript son 0-indexados
            const año = fecha.getFullYear();
    
            fechaCell.innerHTML = `${dia}/${mes}/${año}`;
            planPagoCell.innerHTML = `$${cuotaInicial.toLocaleString('es-ES', { style: 'decimal' })}`;
            mesesCell.innerHTML = fecha.toLocaleString('default', { month: 'long' });
            cuotaCell.innerHTML = `$${valorPorCuota.toLocaleString('es-ES', { style: 'decimal' })}`;
        }
    }else{
        Swal.fire("Plan de pago","Por favor ingrese el numero de coutas","warning")
    }
});

