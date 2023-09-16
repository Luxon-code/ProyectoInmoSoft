from fpdf import FPDF
from datetime import datetime
from appInmoSoft.models import *

class PdfSeparacion(FPDF):
    def header(self):
        # Logo
        self.image('media/Logo.png', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        self.ln()
        # Move to the right
        self.cell(60)
        # Title
        self.cell(80, 10, 'INMOSOFT', 0, 0, 'C')
        self.ln()
        self.cell(60)
        self.cell(80, 10, "Separacion del inmueble" , 0, 0, 'C')
        # Line break
        self.ln(30)

    def footer(self):
        # Pie de página del PDF
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')
        
    def mostrarDatos(self,planPago:PlanDePago):
        #datos del cliente
        self.set_font('Arial','B',14)
        self.cell(0,10,'Datos del Cliente',0,1,'C')
        self.set_font('Arial','B',12)
        self.cell(20,10,'Cedula: ',0,0)
        self.set_font('Arial','',12)
        self.cell(40,10,planPago.plaVenta.venCliente.cliCedula,0,0,'L')
        self.set_font('Arial','B',12)
        self.cell(20,10,"Nombre: ",0,0)
        self.set_font('Arial','',12)
        self.cell(60,10,planPago.plaVenta.venCliente.cliNombre,0,0,'L')
        self.set_font('Arial','B',12)
        self.cell(20,10,"Apellido: ",0,0)
        self.set_font('Arial','',12)
        self.cell(60,10,planPago.plaVenta.venCliente.cliApellido,0,1,'L')
        self.set_font('Arial','B',12)
        self.cell(20,10,"Celular: ",0,0)
        self.set_font('Arial','',12)
        self.cell(40,10,planPago.plaVenta.venCliente.cliTelefono,0,0,'L')
        self.set_font('Arial','B',12)
        self.cell(27,10,"Direccion: ",0,0)
        self.set_font('Arial','',12)
        self.cell(53,10,planPago.plaVenta.venCliente.cliDireccion,0,0,'L')
        self.set_font('Arial','B',12)
        self.cell(30,10,"Estado civil: ",0,0)
        self.set_font('Arial','',12)
        self.cell(60,10,planPago.plaVenta.venCliente.cliEstadoCivil,0,1,'L')
        self.set_font('Arial','B',12)
        self.cell(20,10,"Correo: ",0,0)
        self.set_font('Arial','',12)
        self.cell(0,10,planPago.plaVenta.venCliente.cliCorreo,0,1,'L')
        if planPago.plaVenta.venCliente.cliFamiliar:
            #datos del familiar
            self.set_font('Arial','B',14)
            self.cell(0,10,'Datos del Familiar',0,1,'C')
            self.set_font('Arial','B',12)
            self.cell(20,10,'Cedula: ',0,0)
            self.set_font('Arial','',12)
            self.cell(40,10,planPago.plaVenta.venCliente.cliFamiliar.faCedula,0,0,'L')
            self.set_font('Arial','B',12)
            self.cell(20,10,"Nombre: ",0,0)
            self.set_font('Arial','',12)
            self.cell(60,10,planPago.plaVenta.venCliente.cliFamiliar.faNombre,0,0,'L')
            self.set_font('Arial','B',12)
            self.cell(20,10,"Apellido: ",0,0)
            self.set_font('Arial','',12)
            self.cell(60,10,planPago.plaVenta.venCliente.cliFamiliar.faApellido,0,1,'L')
            self.set_font('Arial','B',12)
            self.cell(20,10,"Celular: ",0,0)
            self.set_font('Arial','',12)
            self.cell(35,10,planPago.plaVenta.venCliente.cliFamiliar.faTelefono,0,0,'L')
            self.set_font('Arial','B',12)
            self.cell(20,10,"Correo: ",0,0)
            self.set_font('Arial','',12)
            self.cell(55,10,planPago.plaVenta.venCliente.cliFamiliar.faCorreo,0,0,'L')
            self.set_font('Arial','B',12)
            self.cell(27,10,"Direccion: ",0,0)
            self.set_font('Arial','',12)
            self.cell(53,10,planPago.plaVenta.venCliente.cliFamiliar.faDireccion,0,1,'L')
        #datos del inmueble
        self.set_font('Arial','B',14)
        self.cell(0,10,'Datos del Inmueble',0,1,'C')
        self.set_font('Arial','B',12)
        self.cell(60,10,'Proyecto al que pertenece: ',0,0)
        self.set_font('Arial','',12)
        self.cell(50,10,planPago.plaVenta.venInmueble.inmProyecto.proNombre,0,0,'L')
        self.set_font('Arial','B',12)
        self.cell(25,10,'Ubicacion: ',0,0)
        self.set_font('Arial','',12)
        self.multi_cell(w=50,h=10,txt=f"{planPago.plaVenta.venInmueble.inmProyecto.proUbicacion.ubiDepartamento},{planPago.plaVenta.venInmueble.inmProyecto.proUbicacion.ubiCuidad}",align='L')
        self.set_font('Arial','B',12)
        self.cell(40,10,'Tipo de proyecto: ',0,0)
        self.set_font('Arial','',12)
        self.cell(20,10,planPago.plaVenta.venInmueble.inmProyecto.proTipo,0,0,'L')
        self.set_font('Arial','B',12)
        self.cell(45,10,'Costo de separacion: ',0,0)
        self.set_font('Arial','',12)
        self.cell(30,10,f"{planPago.plaVenta.venInmueble.inmProyecto.proCostoSeparacion}",0,0,'L')
        self.set_font('Arial','B',12)
        self.cell(27,10,'Direccion: ',0,0,)
        self.set_font('Arial','',12)
        self.cell(50,10,f"{planPago.plaVenta.venInmueble.inmProyecto.proUbicacion.ubiDireccion}",0,1,'L')
        self.set_font('Arial','B',12)
        self.cell(40,10,'Entrega de obra: ',0,0,)
        self.set_font('Arial','',12)
        self.cell(30,10,f"{planPago.plaVenta.venInmueble.inmEntregaDeObra}",0,0,'L')
        if planPago.plaVenta.venInmueble.inmCasa:
            self.set_font('Arial','B',12)
            self.cell(40,10,'Tipo de inmueble: ',0,0,)
            self.set_font('Arial','',12)
            self.cell(30,10,f"{planPago.plaVenta.venInmueble.inmCasa.casCategoria}",0,0,'L')
            self.set_font('Arial','B',12)
            self.cell(20,10,'Precio: ',0,0,)
            self.set_font('Arial','',12)
            self.cell(30,10,f"{planPago.plaVenta.venInmueble.inmCasa.casPrecioVivienda}",0,1,'L')
        else:
            self.set_font('Arial','B',12)
            self.cell(40,10,'Tipo de inmueble: ',0,0,)
            self.set_font('Arial','',12)
            self.cell(30,10,f"{planPago.plaVenta.venInmueble.inmApartamento.apaCategoria}",0,0,'L')
            self.set_font('Arial','B',12)
            self.cell(20,10,'Precio: ',0,0,)
            self.set_font('Arial','',12)
            self.cell(30,10,f"{planPago.plaVenta.venInmueble.inmApartamento.apaPrecioVivienda}",0,1,'L')
        #Plan de pago
        self.set_font('Arial','B',14)
        self.cell(0,10,'Plan de pago',0,1,'C')