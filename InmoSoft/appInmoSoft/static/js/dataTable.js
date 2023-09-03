var idioma =
{
    "sProcessing": "Procesando...",
    "sLengthMenu": "Mostrar _MENU_ registros",
    "sZeroRecords": "No se encontraron resultados",
    "sEmptyTable": "Ningún dato disponible en esta tabla",
    "sInfo": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
    "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
    "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
    "sInfoPostFix": "",
    "sSearch": "Buscar:",
    "sUrl": "",
    "sInfoThousands": ",",
    "sLoadingRecords": "Cargando...",
    "oPaginate": {
        "sFirst": "Primero",
        "sLast": "Último",
        "sNext": "Siguiente",
        "sPrevious": "Anterior"
    },
    "oAria": {
        "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
        "sSortDescending": ": Activar para ordenar la columna de manera descendente"
    },
    "buttons": {
        "copyTitle": 'Informacion copiada',
        "copyKeys": 'Use your keyboard or menu to select the copy command',
        "copySuccess": {
            "_": '%d filas copiadas al portapapeles',
            "1": '1 fila copiada al portapapeles'
        },

        "pageLength": {
            "_": "Mostrar %d filas",
            "-1": "Mostrar Todo"
        }
    }
};

var empresa="INMOSOFT";
var fecha = new Date();
var hoy = fecha.getDate()+"/"+(fecha.getMonth()+1)+"/"+fecha.getFullYear();

/**
 *
 * @param {*} tabla tabla a utilizar
 * @param {*} titulo titulo a colocar en el documento a exportar
 * @param {*} columnas número de columnas en el datatable
 */
function cargarDataTable(tabla,titulo,col){

    var columnas=[];
    for(i=0;i<col;i++){
        columnas.push(i);
    }

    var orientacion = "portrait";

    if (col > 6) {
        orientacion = "landscape";
    }
    tabla.dataTable({
        "paging": true,
        "destroy":true,
        "lengthChange": true,
        "searching": true,
        "ordering": true,
        "info": true,
        "autoWidth": true,
        "language": idioma,
        "lengthMenu": [[5, 20, 50, -1], [5, 20, 50, "Mostrar Todo"]],
        dom: 'Bfrtip',
        buttons: {
            dom: {
                container: {
                    tag: 'div',
                    //className: 'flexcontent'
                },
                buttonLiner: {
                    tag: null
                }
            },
            buttons: [
                {
                    extend: 'pageLength',
                    titleAttr: 'Registros a mostrar',
                    className: 'selectTable'
                },
                {
                    extend: 'copyHtml5',
                    title: empresa,
                    text:'<i class="fa fa-files-o"></i>',
                    messageTop: titulo + "       Fecha: "+hoy,                           
                    exportOptions: {
                        columns:columnas
                    }
                },

                {
                    extend: 'pdfHtml5',
                    footer: true,                    
                    title: empresa,
                    text:'<i class="fa fa-file-pdf-o text-danger"></i>',
                    messageTop: titulo,
                    orientation: orientacion,
                    pageSize: 'LETTER',                  
                    exportOptions: {
                        columns: columnas
                    },
                    customize: function (doc) {
                        doc.content[1].margin = [5, 5, 5, 5],
                        doc.pageMargins = [20, 35, 20,30 ],

                        doc.styles.title = {
                            color: '#6C757D',
                            fontSize: '18',
                            alignment: 'center'
                        },
                        doc.styles.message = {
                            color: '#6C757D',
                            fontSize: '14',
                            alignment: 'center'
                        },

                        doc.styles['td:nth-child(2)'] = {
                            width: '100px',
                            'max-width': '150px'
                        },

                        doc.styles.tableHeader = {
                                fillColor: '#999999',
                                color: 'white',
                                alignment: 'center',
                        },
                        doc["header"] = function() {
                            return {
                                columns: [
                                    {
                                        image: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAgAAAAIACAYAAAD0eNT6AAAAAXNSR0IArs4c6QAAIABJREFUeF7t3QmcHVWV+PFz6nW2DqKizLiAwMiigsoIog4zYtzGXdxaofu9V9WN9iwKKo6OM84QcfDviog6Y5T0WzoBbERkQBEFMoIbKsroAAKCCasiiCzpdCd5df6fagLEkKTfUvVqub98PvNxPh/q3nvO99ykT793q0qFPwgggAACCCDgnIA6lzEJI4AAAggggIDQALAJEEAAAQQQcFCABsDBopMyAggggAACNADsAQQQQAABBBwUoAFwsOikjAACCCCAAA0AewABBBBAAAEHBWgAHCw6KSOAAAIIIEADwB5AAAEEEEDAQQEaAAeLTsoIIIAAAgjQALAHEEAAAQQQcFCABsDBopMyAggggAACNADsAQQQQAABBBwUoAFwsOikjAACCCCAAA0AewABBBBAAAEHBWgAHCw6KSOAAAIIIEADwB5AAAEEEEDAQQEaAAeLTsoIIIAAAgjQALAHEEAAAQQQcFCABsDBopMyAggggAACNADsAQQQQAABBBwUoAFwsOikjAACCCCAAA0AewABBBBAAAEHBWgAHCw6KSOAAAIIIEADwB5AAAEEEEDAQQEaAAeLTsoIIIAAAgjQALAHEEAAAQQQcFCABsDBopMyAggggAACNADsAQQQQAABBBwUoAFwsOikjAACCCCAAA0AewABBBBAAAEHBWgAHCw6KbstMDU1tcvMzMyBntnuYRg+XlVnLQx/N6B621G+f62qmttCZI+AGwI0AG7UmSwdFzhjYmLPTZ53jKq+1MwOU5GBHZD8XkS+q2bnrN+48azx8fFNjtORPgKFFaABKGxpSQwBkXq9Hv2m/2+i+qad/NDfLlUocpuKfH7x4OApQ0NDG/BEAIFiCdAAFKueZIPAnMCKFSsWDC5e/F4x+7CILOqFxURuNNXxarV6US/zMBYBBLIlQAOQrXoQDQI9C6w+7bS9WgMD56nIM3uebMsEZmae6id/vXbtB5cvXx7GNS/zIIBAegI0AOnZszICsQusbjQOC83OFZEnxD55NGEYnjO9adPI+Pj4dCLzMykCCPRNgAagb9QshECyAqsajTeY2SoRGUx2JblSBwZeOzIyckvC6zA9AggkKEADkCAuUyPQL4HJRuM4MTtZRLy+rGl2qyfy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',
                                        width: 50,
                                        height: 50
                                    }
                                ],
                                margin: [40, 20,0,0]
                            }
                        },
                        doc['footer']=(function(page, pages) {
                            return {
                                columns: [
                                    {
                                        text: "Fecha: " + hoy,
                                        alignment: 'lef',
                                        color:'#6C757D',
                                    },
                                    {
                                        text: "Sistema InmoSoft",
                                        alignment: 'center',
                                        color:'#6C757D',
                                    },

                                    {
                                        alignment: 'right',
                                        color:'#6C757D',
                                        text: ['página ', { text: page.toString() },  ' de ', { text: pages.toString() }]
                                    }
                                ],
                                margin: [50, 0]
                            }
                        });


                    }
                },
                {
                    extend: 'excelHtml5',                   
                    title: empresa,
                    text: '<i class="fa fa-file-excel-o text-success"></i>',
                    messageTop: titulo + "       Fecha: "+hoy,                  
                    exportOptions: {
                        columns: columnas
                    },
                },
                {
                    extend: 'csvHtml5',                  
                    title: empresa,
                    text: '<i class="fa fa-file-text-o"></i>',
                    messageTop: titulo + "       Fecha: "+hoy,                   
                    exportOptions: {
                        columns: columnas
                    }
                },
                {
                    extend: 'print',                 
                    title: empresa,
                    text:'<i class="fa fa-print"></i>',
                    messageTop: titulo + "       Fecha: "+hoy,                  
                    exportOptions: {
                        columns: columnas
                    }
                },


            ]
        }
    });
}
