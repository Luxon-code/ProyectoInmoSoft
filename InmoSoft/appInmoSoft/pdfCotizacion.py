from fpdf import FPDF
from PIL import Image
from io import BytesIO
import tempfile

class PdfCotizacion(FPDF):
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
        self.cell(80, 10, "Cotizacion del proyecto" , 0, 0, 'C')
        # Line break
        self.ln(30)

    def footer(self):
        # Pie de página del PDF
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')
        
    def mostrarDatos(self, datos):
        #cliente
        self.set_font('Arial','B',14)
        self.cell(0,10,'Información del Cliente',0,1,'C')
        self.set_font('Arial','B',12)
        self.cell(20,10,'Cedula: ',0,0)
        self.set_font('Arial','',12)
        self.cell(0,10,datos["cedula"],0,1,'L')
        self.set_font('Arial','B',12)
        self.cell(20,10,"Nombre: ",0,0)
        self.set_font('Arial','',12)
        self.cell(0,10,datos["nombre"],0,1,'L')
        self.set_font('Arial','B',12)
        self.cell(20,10,"Apellido: ",0,0)
        self.set_font('Arial','',12)
        self.cell(0,10,datos["apellido"],0,1,'L')
        self.set_font('Arial','B',12)
        self.cell(20,10,"Celular: ",0,0)
        self.set_font('Arial','',12)
        self.cell(0,10,datos["celular"],0,1,'L')
        self.set_font('Arial','B',12)
        self.cell(20,10,"Correo: ",0,0)
        self.set_font('Arial','',12)
        self.cell(0,10,datos["correo"],0,1,'L')
        
        #proyecto
        self.set_font('Arial','B',14)
        self.cell(0,10,'Información del Proyecto',0,0,'C')
        self.ln()
        self.set_font('Arial','B',12)
        self.cell(0,10,datos["nombreProyecto"],0,1,'C')
        # Ruta de la imagen (reemplaza con la ruta de tu imagen)
        imagen_entrada = f'media/{datos["foto"]}'
        # Abre la imagen utilizando Pillow
        imagen = Image.open(imagen_entrada)
        imagen = imagen.convert('RGB')
        
        # Guarda la imagen convertida como un archivo temporal
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        imagen.save(temp_file.name, format='JPEG')
        
        # Muestra la imagen en el PDF
        self.image(temp_file.name, w=100, h=60, x=55)
        self.ln()
        self.cell(0,10,"Descripcion",0,1,"L")
        self.set_font('Arial','',12)
        self.multi_cell(w=0,h=10,txt=datos["descripcion"],align="J")
        self.set_font('Arial','B',12)
        self.cell(40,10,"Tipo de proyecto: ",0,0)
        self.set_font('Arial','',12)
        self.cell(0,10,datos["tipo"],0,1,'L')
        self.set_font('Arial','B',12)
        self.cell(20,10,"Fiducia: ",0,0)
        self.set_font('Arial','',12)
        self.cell(0,10,datos["fiducia"],0,1,'L')
        self.set_font('Arial','B',12)
        self.cell(50,10,"Costo de separacion: ",0,0)
        self.set_font('Arial','',12)
        self.cell(0,10,f'$ {datos["costoSeparacion"]}',0,1,'L')
        self.set_font('Arial','B',12)
        self.cell(60,10,"Precio del inmuble desde: ",0,0)
        self.set_font('Arial','',12)
        self.cell(0,10,f'$ {datos["precio"]}',0,1,'L')
        self.set_font('Arial','B',12)
        self.cell(50,10,"Tipo de Parqueadero: ",0,0)
        self.set_font('Arial','',12)
        self.cell(0,10,datos["parqueadero"],0,1,'L')
        self.set_font('Arial','B',12)
        self.cell(0,10,"Ubicacion del proyecto",0,0,'C')
        self.ln()
        self.set_font('Arial','B',12)
        self.cell(35,10,"Departamento: ",0,0)
        self.set_font('Arial','',12)
        self.cell(0,10,datos["departamento"],0,1,'L')
        self.set_font('Arial','B',12)
        self.cell(30,10,"Municipio: ",0,0)
        self.set_font('Arial','',12)
        self.cell(0,10,datos["municipio"],0,1,'L')
        self.set_font('Arial','B',12)
        self.cell(30,10,"Direccion: ",0,0)
        self.set_font('Arial','',12)
        self.cell(0,10,datos["direccion"],0,1,'L')
        self.ln()
        self.set_font('Arial','I',12)
        self.multi_cell(w=0,h=10,txt="Para mas informacion sobre el proyecto uno de nuestros asesores se comunicara lo mas pronto posible con usted.",align='L')
