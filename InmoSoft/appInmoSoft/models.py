from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
# Create your models here.
tipoUsuario = [
    ('Administrador',"Administrador"),('Asesor', 'Asesor'),
]
tipoCategoriaCasas =[
    ('Tipo A','Tipo A'),('Tipo B','Tipo B'),('Tipo C','Tipo C')
]
tipoCategoriaApartamento =[
    ('Tipo A','Tipo A'),('Tipo B','Tipo B'),('Tipo C','Tipo C'),('Tipo penthouse','Tipo penthouse')
]

entregaDeObra=[
    ('Obra Gris','Obra Gris'),('Obra Blanca','Obra Blanca'),('Obra Full acabado','Obra Full acabado')
]

estadoDeInmueble=[
    ('Disponible','Disponible'), ('Separado','Separado')
]

tipoDeParqueadero=[
    ('Comunal','Comunal'),('Asignado','Asignado'),('Propio','Propio')
]

estadoCivil=[
    ('Soltero','Soltero'),('Casado','Casado')
]

class User(AbstractUser):
    userCedula = models.CharField(max_length=20,unique=True,db_comment="Numero de cedula del usuario")
    userTelefono = models.CharField(max_length=20,db_comment="Numero de telefono del usuario")
    userFoto = models.FileField(upload_to=f"fotos/", null=True, blank=True,db_comment="Foto del Usuario")
    userTipo = models.CharField(max_length=15,choices=tipoUsuario,db_comment="Nombre Tipo de usuario")
    userfechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    userfechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")

    def _str_(self):
        return f"{self.username}"

class Casas(models.Model):
    casNumeroManzana =  models.IntegerField(max_length=20, db_comment="Numero de manzana")
    casNumeroInmueble = models.IntegerField(max_length=20, db_comment="Numero de inmueble")
    casTotalCasas = models.IntegerField(max_length=20, db_comment="Total de casas en el proyecto")
    casCategoria = models.CharField(max_length=15, choices=tipoCategoriaCasas, db_comment="Tipo de casa")
    casPrecioVivienda = models.IntegerField(max_length=20,db_comment="Precio de vivienda") 
    casfechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    casfechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")

    def _str_(self) :
        return f"El numero del inmueble es: {self.casNumeroInmueble}"

class Apartamento(models.Model):
    apaNumeroTorre =  models.IntegerField(max_length=20, db_comment="Numero de Torre")
    apaNumeroInmueble = models.IntegerField(max_length=20, db_comment="Numero de inmueble")
    apaTotalApartamento = models.IntegerField(max_length=20, db_comment="Total de apartamentos en el proyecto")
    apaCategoria = models.CharField(max_length=15, choices=tipoCategoriaApartamento, db_comment="Tipo de apartamento")
    apaPrecioVivienda = models.IntegerField(max_length=20,db_comment="Precio de vivienda") 
    apafechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    apafechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")

    def _str_(self) :
       return f"El numero del inmueble es: {self.apaNumeroInmueble}"

class Ubicacion(models.Model):
    ubiDepartamento =  models.CharField(max_length=20, db_comment="ubicacion del departamento del proyecto")
    ubiCuidad =  models.CharField(max_length=20, db_comment="ubicacion de la cuidad del prouceto")
    ubiDireccion = models.CharField(max_length=20,db_comment="Direccion del proyecto")
    ubifechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    ubifechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")

class Proyecto(models.Model):
    proNombre = models.CharField(max_length=25, db_comment="Nombre del proyecto")
    proDescripcion = models.TextField(max_length=255, db_comment="Descripcion del proyecto")
    proFiducia = models.CharField(max_length=25,db_comment="Fiducia que va a contriduir en el proyecto")
    proParqueadero = models.CharField(max_length=25,choices=tipoDeParqueadero ,db_comment="Tipo de parqueadero que tiene el proyecto")
    profechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    profechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    proUbicacion = models.ForeignKey(Ubicacion,on_delete=models.PROTECT,db_comment="Ubicacion del proyecto")
    
class Inmueble(models.Model):
    inmNumeroHabitaciones = models.IntegerField(max_length=20,db_comment="Numero de habitaciones de un inmueble")
    inmAreaConstruida = models.CharField(max_length=20, db_comment="Area construida del inmueble")
    inmValorInmueble = models.IntegerField(max_length=20, db_comment="Valor del inmueble")
    inmEntregaDeObra =  models.CharField(max_length=20, choices=entregaDeObra ,db_comment="Entrega del inmueble")
    inmEstado = models.CharField(max_length=20,choices=estadoDeInmueble ,db_comment="estado de disponibilidad del Inmueble")
    inmCasa = models.ForeignKey(Casas, on_delete=models.PROTECT,db_comment="hace referencia al tipo de inmueble")
    inmApartamento =  models.ForeignKey(Apartamento, on_delete=models.PROTECT,db_comment="hace refencia al tipo de inmueble")
    inmProyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT, db_comment="prouecto que corresponde el inmueble")
    inmfechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    inmfechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")

       
class Cliente(models.Model):
    cliNombre = models.CharField(max_length=20,db_comment="Nombre del cliente")
    cliApellido = models.CharField(max_length=20,db_comment="Apellido del cliente")
    cliTelefono =  models.CharField(max_length=20, db_comment="Telefono del cliente")
    cliCorreo = models.CharField(max_length=20,db_comment="Correo del cliente")
    cliCedula =  models.CharField(max_length=20, db_comment="cedula del cliente")
    cliDireccion = models.CharField(max_length=20,db_comment="Direccion del cliente")
    cliEstadoCivil =  models.CharField(max_length=20,choices=estadoCivil, db_comment="Estado Civil del cliente")
    cliFechaSeparacion = models.DateField(auto_now=True, db_comment="Fecha Separacion del cliente")
    clifechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    clifechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    
class Venta(models.Model):
    venFechaSeparacion = models.DateField(auto_now=True, db_comment="Fecha Separacion del cliente")
    venFechaCreacion = models.DateField(auto_now=True, db_comment="Fecha de creacion")
    venfechaModificacion =  models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    venUsuario = models.ForeignKey(User,on_delete=models.PROTECT,db_comment="Asesor")
    venInmueble = models.ForeignKey(Inmueble, on_delete=models.PROTECT,db_comment="Inmueble disponible para la venta")
    venCliente = models.ForeignKey(Cliente,on_delete=models.PROTECT,db_column="Cliente interesado en el inmueble")
    
class PlanDePago(models.Model):
    plaFechaInicial = models.DateField(db_comment="Fecha de inicio del plan de pago")
    plaFechaFinal = models.DateField(db_comment="Fecha de final del plan de pago")
    plaCuotaInicial = models.IntegerField(max_length=20, db_comment="Valor de la cuota Inicial")
    plaValorDeCuota = models.IntegerField(max_length=20, db_comment="Valor de la Cuota")
    plafechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora de registro")
    plafechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    plaVenta= models.ForeignKey(Venta, on_delete=models.PROTECT, db_comment="venta")
    
class RegistroPago(models.Model):
    regFechaPago=models.DateField(auto_now=True, db_comment="Fecha de pago")
    regValorPago=models.IntegerField(max_length=20,db_comment="Valor de pagode la cuota")
    regPendiente=models.IntegerField(max_length=20,db_comment="Valor pendiente")
    regRecaudo= models.IntegerField(max_length=20,db_comment="Recaudo total")
    regfechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    regfechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    regPlanDePago = models.ForeignKey(PlanDePago, on_delete=models.PROTECT, db_comment="plan de pago")
