from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
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
    ('Disponible','Disponible'), ('Separado','Separado'),('Vendido','Vendido')
]

tipoDeParqueadero=[
    ('Comunal','Comunal'),('Asignado','Asignado'),('Propio','Propio')
]

estadoCivil=[
    ('Soltero','Soltero'),('Casado','Casado')
]

fiducia=[
    ('Bancolombia','Bancolombia'),('BBVA','BBVA'),('Banco de Bogota','Banco de Bogota'),('Banco Caja Social','Banco Caja Social'),('Grupo Bancolombia','Grupo Bancolombia'),('Davivienda','Davivienda'),('Banco de Occidente','Banco de Occidente')
]
tipoDeProyecto = [
    ('VIS', 'VIS'),('VIP','VIP'),('NO VIS','NO VIS')
]
class User(AbstractUser):
    userCedula = models.CharField(
        max_length=20,unique=True,
        db_comment="Numero de cedula del usuario",
        error_messages={
        'unique': "Ya existe un usuario con esta cedula",
        }
        )
    userTelefono = models.CharField(max_length=20,db_comment="Numero de telefono del usuario")
    userFoto = models.FileField(upload_to=f"fotos/", null=True, blank=True,db_comment="Foto del Usuario")
    userTipo = models.CharField(max_length=15,choices=tipoUsuario,db_comment="Nombre Tipo de usuario")
    username = models.CharField(
        ("username"),
        max_length=150,
        unique=True,
        error_messages={
            "unique": ("Ya existe un usuario con ese correo electronico"),
        },
    )
    email = models.EmailField(("email address"), blank=True,unique=True,
                              error_messages={
            "unique": ("Ya existe un usuario con ese correo electronico"),
        })
    userfechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    userfechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    def _str_(self):
        return f"{self.username}"

class Casas(models.Model):
    casNumeroHabitaciones = models.IntegerField(db_comment="Numero de habitaciones de un inmueble")
    casAreaConstruida = models.CharField(max_length=20, db_comment="Area construida del inmueble")
    casCategoria = models.CharField(max_length=15, choices=tipoCategoriaCasas, db_comment="Tipo de casa")
    casPrecioVivienda = models.BigIntegerField(db_comment="Precio de vivienda") 
    casfechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    casfechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")

    def _str_(self) :
        return f"El numero del inmueble es: {self.casNumeroInmueble}"

class Apartamento(models.Model):
    apaNumeroHabitaciones = models.IntegerField(db_comment="Numero de habitaciones de un inmueble")
    apaAreaConstruida = models.CharField(max_length=20, db_comment="Area construida del inmueble")
    apaCategoria = models.CharField(max_length=15, choices=tipoCategoriaApartamento, db_comment="Tipo de apartamento")
    apaPrecioVivienda = models.BigIntegerField(db_comment="Precio de vivienda") 
    apafechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    apafechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")

class Ubicacion(models.Model):
    ubiDepartamento =  models.CharField(max_length=255, db_comment="ubicacion del departamento del proyecto")
    ubiCuidad =  models.CharField(max_length=255, db_comment="ubicacion de la cuidad del prouceto")
    ubiDireccion = models.CharField(max_length=255,db_comment="Direccion del proyecto")
    ubifechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    ubifechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")

class Proyecto(models.Model):
    proNombre = models.CharField(max_length=25, db_comment="Nombre del proyecto")
    proDescripcion = models.TextField(max_length=255, db_comment="Descripcion del proyecto")
    proTipo = models.CharField(max_length=255,choices=tipoDeProyecto,db_comment="Tipo de proyecto",default='VIS')
    proFiducia = models.CharField(max_length=25,choices=fiducia,db_comment="Fiducia que va a contriduir en el proyecto")
    proFoto = models.FileField(upload_to=f"fotosPro/", null=True, blank=True,db_comment="Foto del Proyecto")
    proNumeroManzanasTorres =  models.IntegerField(db_comment="Numero de manzanas o torres")
    proCostoSeparacion = models.BigIntegerField(db_comment="Costo de separacion del inmuble")
    proEstado = models.BooleanField(default=True,db_comment="Estado")
    proNumeroInmuebles = models.IntegerField(db_comment="Numero de inmueble por manzanas o torres")
    proNumeroDePisos = models.IntegerField(db_comment="Numero de pisos")
    proTotalInmuebles = models.IntegerField(db_comment="Total de inmuebles en todo el proyecto")
    proParqueadero = models.CharField(max_length=25,choices=tipoDeParqueadero ,db_comment="Tipo de parqueadero que tiene el proyecto")
    proCantidadParqueadero = models.BigIntegerField(db_comment='Cantidad de parqueaderos que tendra el proyecto')
    profechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    profechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    proUbicacion = models.ForeignKey(Ubicacion,on_delete=models.PROTECT,db_comment="Ubicacion del proyecto")
    
class fotoInmuble(models.Model):
    fotInmuble = models.FileField(upload_to=f"fotosInm/", null=True, blank=True,db_comment="Fotos del Imueble")
    fotProyecto = models.ForeignKey(Proyecto,on_delete=models.PROTECT,db_comment="llave foranea para defenir a que proyecto pertenece la foto del inmuble") 
    fotfechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fotfechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
class Inmueble(models.Model):
    inmEntregaDeObra =  models.CharField(max_length=20, choices=entregaDeObra ,db_comment="Entrega del inmueble")
    inmEstado = models.CharField(max_length=20,choices=estadoDeInmueble ,db_comment="estado de disponibilidad del Inmueble")
    inmCasa = models.ForeignKey(Casas, on_delete=models.PROTECT,db_comment="hace referencia al tipo de inmueble",null=True)
    inmApartamento =  models.ForeignKey(Apartamento, on_delete=models.PROTECT,db_comment="hace refencia al tipo de inmueble",null=True)
    inmProyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT, db_comment="proyecto al que corresponde el inmueble")
    inmfechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    inmfechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")


class Familiar(models.Model):
    faNombre= models.CharField(max_length=20,db_comment="Nombre del familiar")
    faApellido = models.CharField(max_length=20,db_comment="Apellido del familiar")
    faTelefono =  models.CharField(max_length=20, db_comment="Telefono del familiar")
    faCorreo = models.CharField(max_length=20,db_comment="Correo del familiar")
    faCedula =  models.CharField(max_length=20, db_comment="cedula del familiar")
    faDireccion = models.CharField(max_length=20,db_comment="Direccion del familiar")
    fafechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fafechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")

class Cliente(models.Model):
    cliNombre = models.CharField(max_length=20,db_comment="Nombre del cliente")
    cliApellido = models.CharField(max_length=20,db_comment="Apellido del cliente")
    cliTelefono =  models.CharField(max_length=20, db_comment="Telefono del cliente")
    cliCorreo = models.CharField(max_length=20,db_comment="Correo del cliente")
    cliFamiliar=models.ForeignKey(Familiar,on_delete=models.PROTECT,db_comment="Familiar del cliente",null=True)
    cliCedula =  models.CharField(max_length=20, db_comment="cedula del cliente")
    cliDireccion = models.CharField(max_length=20,db_comment="Direccion del cliente")
    cliEstadoCivil =  models.CharField(max_length=20,choices=estadoCivil, db_comment="Estado Civil del cliente")
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
    plaNumCuota= models.IntegerField(db_comment="Numero de cuotas")
    plaCuotaInicial = models.IntegerField(db_comment="Valor de la cuota Inicial")
    plaValorDeCuota = models.IntegerField(db_comment="Valor de la Cuota")
    plafechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora de registro")
    plafechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    plaVenta= models.ForeignKey(Venta, on_delete=models.PROTECT, db_comment="venta")
    
class RegistroPago(models.Model):
    regFechaPago=models.DateField(auto_now=True, db_comment="Fecha de pago")
    regValorPago=models.IntegerField(db_comment="Valor de pagode la cuota")
    regPendiente=models.IntegerField(db_comment="Valor pendiente")
    regRecaudo= models.IntegerField(db_comment="Recaudo total")
    regfechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    regfechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    regPlanDePago = models.ForeignKey(PlanDePago, on_delete=models.PROTECT, db_comment="plan de pago")
