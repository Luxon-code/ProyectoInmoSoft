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
        self.cell(0,10,planPago.plaVenta.venCliente.cliCedula,0,1,'L')
        self.set_font('Arial','B',12)
        self.cell(20,10,"Nombre: ",0,0)
        self.set_font('Arial','',12)
        self.cell(0,10,planPago.plaVenta.venCliente.cliNombre,0,1,'L')
        self.set_font('Arial','B',12)
        self.cell(20,10,"Apellido: ",0,0)
        self.set_font('Arial','',12)
        self.cell(0,10,planPago.plaVenta.venCliente.cliApellido,0,1,'L')
        self.set_font('Arial','B',12)
        self.cell(20,10,"Celular: ",0,0)
        self.set_font('Arial','',12)
        self.cell(0,10,planPago.plaVenta.venCliente.cliTelefono,0,1,'L')
        self.set_font('Arial','B',12)
        self.cell(20,10,"Correo: ",0,0)
        self.set_font('Arial','',12)
        self.cell(0,10,planPago.plaVenta.venCliente.cliCorreo,0,1,'L')
        self.set_font('Arial','B',12)
        self.cell(27,10,"Direccion: ",0,0)
        self.set_font('Arial','',12)
        self.cell(0,10,planPago.plaVenta.venCliente.cliDireccion,0,1,'L')
        self.set_font('Arial','B',12)
        self.cell(30,10,"Estado civil: ",0,0)
        self.set_font('Arial','',12)
        self.cell(0,10,planPago.plaVenta.venCliente.cliEstadoCivil,0,1,'L')
        if planPago.plaVenta.venCliente.cliFamiliar:
            #datos del familiar
            self.set_font('Arial','B',14)
            self.cell(0,10,'Datos del Familiar',0,1,'C')
            self.set_font('Arial','B',12)
            self.cell(20,10,'Cedula: ',0,0)
            self.set_font('Arial','',12)
            self.cell(0,10,planPago.plaVenta.venCliente.cliFamiliar.faCedula,0,1,'L')
            self.set_font('Arial','B',12)
            self.cell(20,10,"Nombre: ",0,0)
            self.set_font('Arial','',12)
            self.cell(0,10,planPago.plaVenta.venCliente.cliFamiliar.faNombre,0,1,'L')
            self.set_font('Arial','B',12)
            self.cell(20,10,"Apellido: ",0,0)
            self.set_font('Arial','',12)
            self.cell(0,10,planPago.plaVenta.venCliente.cliFamiliar.faApellido,0,1,'L')
            self.set_font('Arial','B',12)
            self.cell(20,10,"Celular: ",0,0)
            self.set_font('Arial','',12)
            self.cell(0,10,planPago.plaVenta.venCliente.cliFamiliar.faTelefono,0,1,'L')
            self.set_font('Arial','B',12)
            self.cell(20,10,"Correo: ",0,0)
            self.set_font('Arial','',12)
            self.cell(0,10,planPago.plaVenta.venCliente.cliFamiliar.faCorreo,0,1,'L')
            self.set_font('Arial','B',12)
            self.cell(27,10,"Direccion: ",0,0)
            self.set_font('Arial','',12)
            self.cell(0,10,planPago.plaVenta.venCliente.cliFamiliar.faDireccion,0,1,'L')