/// Obtén el valor de la cuota inicial y el número de cuotas ingresados por el usuario
const numCuotasInput = document.getElementById("txtNumeroCuotas");
const fechaInicialInput = document.getElementById("fechaInicio");
const resultadoTabla = document.getElementById("tablaPlan");

// Agrega un event listener para calcular el plan de pago cuando se haga clic en el botón "Calcular Plan"
document.getElementById("btnCalcularPlan").addEventListener("click", function () {
    if (numCuotasInput.value !== "" && fechaInicialInput.value !== "") {
        const numCuotas = parseInt(numCuotasInput.value);
        // Obtenemos el valor del inmueble desde el elemento HTML
        var valorInmueble = parseFloat(document.getElementById('precioInmuble').value);
        var valorSeparacion = parseFloat(document.getElementById('costoSeparacion').value);
    
        // Calculamos el 30% del valor del inmueble
        var cuotaInicial = Math.round(valorInmueble * 0.3);
        // Calcula el valor de cada cuota mensual
        const valorPorCuota = Math.round((cuotaInicial - valorSeparacion) / numCuotas);

        document.getElementById("cuotaInicial").value = cuotaInicial;
        valorCuota.value = valorPorCuota;

        // Limpia la tabla existente
        resultadoTabla.innerHTML = "";

        // Parsea la fecha inicial ingresada por el usuario
        const fechaInicial = new Date(fechaInicialInput.value);
    
        // Llena la tabla con los detalles del plan de pago
        for (let i = 0; i < numCuotas; i++) {
            const fecha = new Date(fechaInicial);
            fecha.setMonth(fecha.getMonth() + i);

            const newRow = resultadoTabla.insertRow();
            const fechaCell = newRow.insertCell(0);
            const planPagoCell = newRow.insertCell(1);
            const mesesCell = newRow.insertCell(2);
            const cuotaCell = newRow.insertCell(3);

            // Obtén el día, el mes y el año de la fecha
            const dia = fecha.getDate()+1;
            const mes = fecha.getMonth() + 1; // Suma 1 ya que los meses en JavaScript son 0-indexados
            const año = fecha.getFullYear();

            fechaCell.innerHTML = `${dia}/${mes}/${año}`;
            planPagoCell.innerHTML = `$ ${cuotaInicial.toLocaleString('es-ES', { style: 'decimal' })} COP`;
            mesesCell.innerHTML = fecha.toLocaleString('default', { month: 'long' });
            cuotaCell.innerHTML = `$ ${valorPorCuota.toLocaleString('es-ES', { style: 'decimal' })} COP`;
        }

        // Calcula la fecha final sumando el número de cuotas a la fecha inicial
        const fechaFinal = new Date(fechaInicial);
        fechaFinal.setMonth(fechaFinal.getMonth() + numCuotas - 1);
        const diaFinal = fechaFinal.getDate()+1;
        const mesFinal = fechaFinal.getMonth() + 1;
        const añoFinal = fechaFinal.getFullYear();

        // Muestra la fecha final en algún lugar de tu interfaz si es necesario
        document.getElementById("fechaFinal").value = `${diaFinal}/${mesFinal}/${añoFinal}`;
    } else {
        Swal.fire("Plan de pago", "Por favor ingrese el número de cuotas y la fecha inicial", "warning")
    }
});
