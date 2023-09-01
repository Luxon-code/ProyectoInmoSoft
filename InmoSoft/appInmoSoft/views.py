from datetime import date, datetime
from django.shortcuts import render, redirect
from appInmoSoft.models import *
from django.contrib.auth.models import Group
from django.db import Error, transaction
from django.core.files.base import ContentFile
import random
import string
import base64
from django.contrib.auth import authenticate
from django.contrib import auth
from django.conf import settings
from .decorators import soloAdmin,soloAsesor
import os
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
import threading
import requests
from smtplib import SMTPException
from django.http import JsonResponse
from django.db.models import Sum, Avg, Count
from django.core.exceptions import ValidationError
# Create your views here.

#-------VISTAS----------
@soloAdmin
def vistaRegistrarUsuario(request):
    if request.user.is_authenticated: 
        roles = Group.objects.all()
        retorno = {'roles': roles,'user':request.user}
        return render(request,'administrador/registrarUsuario.html',retorno)
    else:
        mensaje = "Debe iniciar sesión"
        return render(request,'inicioSesion.html',{"mensaje":mensaje})
@soloAdmin
def vistaModificarUsuario(request):
    if request.user.is_authenticated:
        retorno = {"user":request.user}
        return render(request,'administrador/modificarUsuario.html',retorno)
    else:
        mensaje = "Debe iniciar sesión"
        return render(request,'inicioSesion.html',{"mensaje":mensaje})

def vistaPaginaPrincipal(request):
    return render(request,'paginaPrincipal.html')

def vistaIniciarSesion(request):
    return render(request,'inicioSesion.html')

@soloAdmin
def vistaInicioAdministrador(request):
    if request.user.is_authenticated:
        retorno = {"user":request.user}
        return render(request,'administrador/inicioAdministrador.html',retorno)
    else:
        mensaje = "Debe iniciar sesión"
        return render(request,'inicioSesion.html',{"mensaje":mensaje}) 
    
@soloAsesor
def vistaInicioAsesor(request):
    if request.user.is_authenticated:
        retorno = {"user":request.user}  
        return render(request,'asesor/inicioAsesor.html',retorno)
    else:
        mensaje = "Debe iniciar sesión"
        return render(request,'inicioSesion.html',{"mensaje":mensaje})

def vistaPerfilUsuario(request):
    if request.user.is_authenticated:
        if request.user.userTipo == 'Administrador':
            retorno = {"user":request.user}  
            return render(request,'administrador/perfilUsuario.html',retorno)
        else:
            retorno = {"user":request.user}  
            return render(request,'asesor/perfilUsuario.html',retorno) 
    else:
        mensaje = "Debe iniciar sesión"
        return render(request,'inicioSesion.html',{"mensaje":mensaje})
@soloAdmin
def vistaRegistrarProyecto(request):
    if request.user.is_authenticated:
        retorno = {"user":request.user,'entregaObra':entregaDeObra,'parqueaderos':tipoDeParqueadero, 'fiducia':fiducia}  
        return render(request,'administrador/registrarProyecto.html',retorno)
    else:
        mensaje = "Debe iniciar sesión"
        return render(request,'inicioSesion.html',{"mensaje":mensaje})

@soloAdmin
def vistaRegistrarCasaoApartamento(request):
    if request.user.is_authenticated:
        retorno = {"user":request.user}  
        return render(request,'administrador/registrarCasaoApartamento.html',retorno)
    else:
        mensaje = "Debe iniciar sesión"
        return render(request,'inicioSesion.html',{"mensaje":mensaje})
    

def vistaDetalleInmueble(request, proyecto_id):
        proyect = Proyecto.objects.filter(id=proyecto_id).first()
        inmueble = Inmueble.objects.filter(inmProyecto=proyect.id).first()
        
        if inmueble.inmCasa:
                proyecto = {
                    'id': proyect.id,
                    'nombre': proyect.proNombre,
                    'ubicacion':proyect.proUbicacion.ubiDepartamento +","+proyect.proUbicacion.ubiCuidad,
                    'descripcion':proyect.proDescripcion,
                    'parqueadero':proyect.proParqueadero,
                    'areaConstruida':inmueble.inmCasa.casAreaConstruida,
                    'foto':proyect.proFoto,
                    'precio':inmueble.inmCasa.casPrecioVivienda,
                    'numInmuebles':proyect.proTotalInmuebles,
                    'numdivision':proyect.proNumeroManzanasTorres,
                    'tipo':"Casas",
                    'division':"Manzanas",
                }
        else:
                proyecto = {
                    'id':proyect.id,
                    'nombre': proyect.proNombre,
                    'ubicacion':proyect.proUbicacion.ubiDepartamento +","+proyect.proUbicacion.ubiCuidad,
                    'descripcion':proyect.proDescripcion,
                    'parqueadero':proyect.proParqueadero,
                    'areaConstruida':inmueble.inmApartamento.apaAreaConstruida,
                    'foto':proyect.proFoto,
                    'precio':inmueble.inmApartamento.apaPrecioVivienda,
                    'numInmuebles':proyect.proTotalInmuebles,
                    'numdivision':proyect.proNumeroManzanasTorres,
                    'tipo':"apartamento",
                    'division':"Torres",
                }
        if request.user.is_authenticated:
            retorno = {'proyecto':proyecto,"user":request.user}
            return render(request, 'asesor/detalleInmueble.html', retorno)
        else:
            retorno = {'proyecto':proyecto}
            return render(request, 'detalleInmueble.html', retorno)
        
    
@soloAdmin
def vistaModificarProyecto(request):
    if request.user.is_authenticated:
        retorno = {"user":request.user,'entregaObra':entregaDeObra,'parqueaderos':tipoDeParqueadero, 'fiducia':fiducia}  
        return render(request,'administrador/modificarProyectos.html',retorno)
    else:
        mensaje = "Debe iniciar sesión"
        return render(request,'inicioSesion.html',{"mensaje":mensaje})
    
        
#-------------------------------------FUNCIONES--------------------------#       

def registrarUsuario(request):
    try:
        cedula = request.POST["txtCedula"]
        nombres = request.POST["txtNombres"]
        apellidos = request.POST["txtApellido"]
        correo = request.POST["txtCorreo"]
        telefono = request.POST["txtTelefono"]
        foto = request.FILES.get("fileFoto")
        idRol = int(request.POST["cbRol"])
        with transaction.atomic():
            # obtener el Rol de acuerdo a id del rol
            rol = Group.objects.get(pk=idRol)
            # crear un objeto de tipo User
            user = User(username=correo, first_name=nombres,
                        last_name=apellidos, email=correo, userTipo=rol.name, userFoto=foto,userCedula=cedula,userTelefono=telefono)
            user.save()
            # agregar el usuario a ese Rol
            user.groups.add(rol)
            # si el rol es Administrador se habilita para que tenga acceso al sitio web del administrador
            if (rol.name == "Administrador"):
                user.is_staff = True 
            # guardamos el usuario con lo que tenemos
            user.save()
            # llamamos a la funcion generarPassword
            passwordGenerado = generarPassword()
            # con el usuario creado llamamos a la función set_password que
            # # encripta el password y lo agrega al campo password del user.
            user.set_password(passwordGenerado)
            # se actualiza el user
            user.save()
            mensaje = "Usuario Agregado Correctamente"
            retorno = {"mensaje": mensaje,"estado":True,'roles':Group.objects.all()}
            # enviar correo al usuario
            asunto = 'Registro Sistema InmoSoft'
            mensajeCorreo = f'Cordial saludo, <b>{user.first_name} {user.last_name}</b>, nos permitimos.\
                informarle que usted ha sido registrado en el Sistema de Inmosoft de la ciudad de Neiva.\
                Nos permitimos enviarle las credenciales de Ingreso a nuestro sistema.<br>\
                <br><b>Username: </b> {user.username}\
                <br><b>Password: </b> {passwordGenerado}\
                <br><br>Lo invitamos a ingresar a nuestro sistema en la url:\
                http://Inmosoft.com'
            thread = threading.Thread(
                target=enviarCorreo, args=(asunto, mensajeCorreo, user.email))
            thread.start()
            return render(request, 'administrador/registrarUsuario.html',retorno)
    except Exception as error:
        transaction.rollback()
        if 'userCedula' in str(error):
            mensaje = "Ya existe un usuario con esta cedula"
        elif 'user.username' in str(error):
            mensaje = "Ya existe un usuario con este correo electronico"
        else:
            mensaje = error
    retorno = {"mensaje": mensaje,"estado":False,'roles':Group.objects.all(),
                "cedula" : cedula,"nombres" : nombres,"apellidos" : apellidos,
                "correo" : correo,"telefono" : telefono
                }
    return render(request, "administrador/registrarUsuario.html",retorno)
def enviarCorreo(asunto=None, mensaje=None, destinatario=None):
    remitente = settings.EMAIL_HOST_USER
    template = get_template('enviarCorreo.html')
    contenido = template.render({
        'destinatario': destinatario,
        'mensaje': mensaje,
        'asunto': asunto,
        'remitente': remitente,
    })
    try:
        correo = EmailMultiAlternatives(
            asunto, mensaje, remitente, [destinatario])
        correo.attach_alternative(contenido, 'text/html')
        correo.send(fail_silently=True)
    except SMTPException as error:
        print(error)
        
def generarPassword():
    """
    Genera un password de longitud de 10 que incluye letras mayusculas
    y minusculas,digitos y cararcteres especiales
    Returns:
        _str_: retorna un password
    """
    longitud = 10

    caracteres = string.ascii_lowercase + \
        string.ascii_uppercase + string.digits
    password = ''

    for i in range(longitud):
        password += ''.join(random.choice(caracteres))
    return password

def getUsuarios(request):
    try:
        retorno = {
            "usuarios":list(User.objects.all().values()),
        }
        return JsonResponse(retorno)
    except Error as error:
        mensaje=f"{error}"
        
def cambiarEstadoUsuario(request,id):
    estado = False
    try:
        with transaction.atomic():
            user = User.objects.get(pk=id)
            if user.is_superuser:
                mensaje = "Este usuario no se le puede cambiar el estado, ya que es el superuser del sistema"
                estado = False
            else:
                if user.is_active:
                    user.is_active = False
                else:
                    user.is_active = True
                user.save()
                estado = True
                mensaje = "Estado del usuario modificado"
    except Error as error:
        transaction.rollback()
        mensaje = f"{error}"
    retorno = {
        'estado': estado,
        'mensaje':mensaje
    }
    
    return JsonResponse(retorno)

def iniciarSesion(request):
    if request.method == 'POST':
        recaptcha_token = request.POST.get('recaptchaToken')
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data={
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_token
        })

        if response.json().get('success') == True:
            username = request.POST["txtUsuario"]
            password = request.POST["txtContraseña"]
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
            # registrar la variable de sesión
                auth.login(request, user)
                if user.groups.filter(name='Administrador').exists():
                    return redirect('/inicioAdministrador/')
                else:
                    return redirect('/inicioAsesor/')
            else:
                mensaje = "El Usuario o Contraseña Son Incorrectas"
                return render(request, "inicioSesion.html", {"mensaje": mensaje})
        else:
            mensaje = "validar recapcha"
            return render(request, "inicioSesion.html", {"mensaje": mensaje})
def iniciarSesionAPI(request,usuario,contraseña):
    username = usuario
    password = contraseña
    user = authenticate(username=username, password=password)
    print(user)
    if user is not None:
    # registrar la variable de sesión
        auth.login(request, user)
        if user.groups.filter(name='Administrador').exists():
           return JsonResponse({'mensaje':'Inicio de sesión exitoso como administrador','estado':True,'username':request.user.username,
                                'correo':request.user.email,'nombre':request.user.first_name,'apellidos':request.user.last_name,
                                'foto':str(request.user.userFoto)})
        else:
            return JsonResponse({'mensaje':'Inicio de sesión exitoso como asesor','estado':True,'username':request.user.username,
                                'correo':request.user.email,'nombre':request.user.first_name,'apellidos':request.user.last_name,
                                'foto':str(request.user.userFoto)})
    else:
        mensaje = "El Usuario o Contraseña Son Incorrectas"
        return JsonResponse({'mensaje':mensaje,'estado':False,'username':"",
                                'correo':"",'nombre':"",'apellidos':"",
                                'foto':""})

def cerrarSesion(request):
    auth.logout(request)
    return render(request, "inicioSesion.html",
                  {"mensaje": "Ha cerrado la sesión"})
    
def modificarDatosUserPerfil(request,id):
    if request.method == "POST":
        try:
            cedula = request.POST["txtCedula"]
            nombres = request.POST["txtNombres"]
            apellidos = request.POST["txtApellido"]
            correo = request.POST["txtCorreo"]
            telefono = request.POST["txtTelefono"]
            foto = request.FILES.get("fileFoto", False)
            username = request.POST["txtUserName"]
            with transaction.atomic():
                user = User.objects.get(pk=id)
                user.username=username
                user.first_name=nombres
                user.last_name=apellidos
                user.email=correo
                user.userCedula=cedula
                user.userTelefono=telefono
                if(foto):
                    if user.userFoto == "":
                        user.userFoto=foto
                    else:
                        os.remove('./media/'+str(user.userFoto))
                        user.userFoto=foto
                user.save()
                mensaje = "Datos Modificados Correctamente"
                retorno = {"mensaje": mensaje,"estado":True}
                if user.userTipo == "Administrador":
                    return render(request, 'administrador/perfilUsuario.html',retorno)
                else:
                    return render(request, 'asesor/perfilUsuario.html',retorno)
        except Error as error:
            transaction.rollback()
            if 'userCedula' in str(error):
                mensaje = "Ya existe un usuario con esta cedula"
            elif 'user.username' in str(error):
                mensaje = "Ya existe un usuario con este nombre de usuario"
            elif 'user.email' in str(error):
                mensaje = "Ya existe un usuario con ese correo electronico"
            else:
                mensaje = error
        retorno = {"mensaje":mensaje,"estado":False}
        if user.userTipo == "Administrador":
            return render(request, 'administrador/perfilUsuario.html',retorno)
        else:
            return render(request, 'asesor/perfilUsuario.html',retorno)
        
def cambiarContraseñaUsuario(request,id):
    if request.method == 'POST':
        try:
            contraseñaActual = request.POST['txtContraseñaActual']
            nuevaContraseña = request.POST['txtNuevaContraseña']
            confirmarContraseña = request.POST['txtConfirmarContraseña']
            with transaction.atomic():
                user = User.objects.get(pk=id)
                if user.check_password(contraseñaActual):
                    if nuevaContraseña == confirmarContraseña:
                        user.set_password(nuevaContraseña)
                        user.save()
                        return redirect('/vistaPerfilUsuario/')
                    else:
                        mensaje="La nueva Contraseña no es igual a la contraseña escrita en confirmar contraseña"
                        retorno={"mensaje":mensaje,"estado":False}
                else:
                    mensaje="No se pudo cambiar la contraseña debido a que la contraseña actual ingresada no es correcta"
                    retorno={"mensaje":mensaje,"estado":False}
                if user.userTipo == "Administrador":
                    return render(request, 'administrador/perfilUsuario.html',retorno)
                else:
                    return render(request, 'asesor/perfilUsuario.html',retorno)
        except Error as error:
            transaction.rollback()
            mensaje = f"{error}"
        retorno = {"mensaje":mensaje,"estado":False}
        if user.userTipo == "Administrador":
            return render(request, 'administrador/perfilUsuario.html',retorno)
        else:
            return render(request, 'asesor/perfilUsuario.html',retorno)

datosForm1 = {}
def datosFormulario1(request):
    datosForm1 = {
        'nombreProyecto': request.POST.get('txtNombreProyecto'),
        'fiducia': request.POST.get('cbFiducia'),
        'numeroTorresOManzanas': int(request.POST.get('txtNumeroTorresoManzanas')),
        'numeroApartamentosOCasas': int(request.POST.get('txtNumerosApartamentosoCasas')),
        'numeroPisos':int(request.POST.get('txtPisos')),
        'totalInmuebles': int(request.POST.get('txtTotalInmuebles')),
        'obraEntregable': request.POST.get('cbObraentregable'),
        'parqueadero': request.POST.get('cbParqueadero'),
        'departamento': request.POST.get('cbDepartamento'),
        'ciudad': request.POST.get('cbMunicipio'),
        'direccion': request.POST.get('txtDireccion'),
        'descripcion': request.POST.get('txtDescripcion'),
    }
    fotoProyecto = request.FILES.get("fileFoto")
    if fotoProyecto:
        foto_base64 = base64.b64encode(fotoProyecto.read()).decode('utf-8')
        request.session['fotoProyecto'] = foto_base64

    return render(request, 'administrador/registrarCasaoApartamento.html', datosForm1)

def registrarProyecto(request):
    if request.method == 'POST':
        try:
            tipoProyecto = request.POST.get('tipoProyecto')
            if(tipoProyecto=='Casa'):
                nombreProyecto= request.POST.get('txtNombreProyecto')
                fiducia= request.POST.get('cbFiducia')
                numeroTorresOManzanas= int(request.POST.get('txtNumeroTorresoManzanas'))
                numeroApartamentosOCasas= int(request.POST.get('txtNumerosApartamentosoCasas'))
                numeroPisos=int(request.POST.get('txtPisos'))
                totalInmuebles= int(request.POST.get('txtTotalInmuebles'))
                obraEntregable= request.POST.get('cbObraentregable')
                parqueadero= request.POST.get('cbParqueadero')
                departamento= request.POST.get('cbDepartamento')
                ciudad= request.POST.get('cbMunicipio')
                direccion= request.POST.get('txtDireccion')
                descripcion= request.POST.get('txtDescripcion')
                numeroHabitaciones=request.POST.get('txtNumHabitaciones')
                areaConstruida=request.POST.get('txtAreaConstruida')
                fotosInmuble = request.FILES.getlist('fileFotosCasa')
                numeroInmubleTipoA = int(request.POST.get('txtNumtipoA'))
                precioTipoA = request.POST.get('txtPrecioA')
                numeroInmubleTipoB = int(request.POST.get('txtNumtipoB'))
                precioTipoB = request.POST.get('txtPrecioB')
                numeroInmubleTipoC = int(request.POST.get('txtNumtipoC'))
                precioTipoC = request.POST.get('txtPrecioC')
                foto_base64 = request.session.get('fotoProyecto', None)
                fotoProyecto = None  # Inicializar con valor None

                if foto_base64:
                    foto_bytes = base64.b64decode(foto_base64)
                    fotoProyecto = ContentFile(foto_bytes, name='foto_proyecto.jpg')
                with transaction.atomic():
                    #Guardamos la ubicacion del proyecto
                    ubicacion = Ubicacion(ubiDepartamento=departamento,
                                          ubiCuidad=ciudad,
                                          ubiDireccion=direccion)
                    ubicacion.save()
                    #guardamos el proyecto
                    proyecto = Proyecto(proNombre=nombreProyecto,
                                        proDescripcion=descripcion,
                                        proFiducia=fiducia,
                                        proFoto=fotoProyecto,
                                        proNumeroManzanasTorres=numeroTorresOManzanas,
                                        proNumeroInmuebles=numeroApartamentosOCasas,
                                        proNumeroDePisos=numeroPisos,
                                        proTotalInmuebles=totalInmuebles,
                                        proParqueadero=parqueadero,
                                        proUbicacion=ubicacion)
                    proyecto.save()
                    #creamos 3 objetos casas segun su tipo
                    casaA = Casas(casNumeroHabitaciones=numeroHabitaciones,
                                        casAreaConstruida=areaConstruida,
                                        casCategoria="Tipo A",
                                        casPrecioVivienda=precioTipoA)
                    casaA.save()
                    casaB = Casas(casNumeroHabitaciones=numeroHabitaciones,
                                        casAreaConstruida=areaConstruida,
                                        casCategoria="Tipo B",
                                        casPrecioVivienda=precioTipoB)
                    casaB.save()
                    casaC = Casas(casNumeroHabitaciones=numeroHabitaciones,
                                        casAreaConstruida=areaConstruida,
                                        casCategoria="Tipo C",
                                        casPrecioVivienda=precioTipoC)
                    casaC.save()
                    #creamos los inmubles segun el numero de su tipo
                    for i in range(numeroInmubleTipoA):
                        inmueble = Inmueble(inmEntregaDeObra=obraEntregable,
                                            inmEstado="Disponible",
                                            inmCasa=casaA,
                                            inmProyecto=proyecto)
                        inmueble.save()
                    for i in range(numeroInmubleTipoB):
                        inmueble = Inmueble(inmEntregaDeObra=obraEntregable,
                                            inmEstado="Disponible",
                                            inmCasa=casaB,
                                            inmProyecto=proyecto)
                        inmueble.save()
                    for i in range(numeroInmubleTipoC):
                        inmueble = Inmueble(inmEntregaDeObra=obraEntregable,
                                            inmEstado="Disponible",
                                            inmCasa=casaC,
                                            inmProyecto=proyecto)
                        inmueble.save()
                    #gurdamos la fotos del inmueble que pertenencen al proyecto creado
                    for foto in fotosInmuble:
                        fotoInm = fotoInmuble(fotInmuble=foto,fotProyecto=proyecto)
                        fotoInm.save()
                    mensaje="Proyecto Registrado Exitosamente" 
                    retorno = {"mensaje":mensaje,"estado":True,"titulo":"Registro de Proyecto"} 
                    return render(request, 'administrador/inicioAdministrador.html',retorno)
            elif(tipoProyecto=='Apartamento'):
                nombreProyecto= request.POST.get('txtNombreProyecto')
                fiducia= request.POST.get('cbFiducia')
                numeroTorresOManzanas= int(request.POST.get('txtNumeroTorresoManzanas'))
                numeroApartamentosOCasas= int(request.POST.get('txtNumerosApartamentosoCasas'))
                numeroPisos=int(request.POST.get('txtPisos'))
                totalInmuebles= int(request.POST.get('txtTotalInmuebles'))
                obraEntregable= request.POST.get('cbObraentregable')
                parqueadero= request.POST.get('cbParqueadero')
                departamento= request.POST.get('cbDepartamento')
                ciudad= request.POST.get('cbMunicipio')
                direccion= request.POST.get('txtDireccion')
                descripcion= request.POST.get('txtDescripcion')
                numeroHabitaciones=request.POST.get('txtNumHabitaciones')
                areaConstruida=request.POST.get('txtAreaConstruida')
                fotosInmuble = request.FILES.getlist('fileFotosApartamento')
                numeroInmubleTipoA = int(request.POST.get('txtNumtipoA'))
                precioTipoA = request.POST.get('txtPrecioA')
                numeroInmubleTipoB = int(request.POST.get('txtNumtipoB'))
                precioTipoB = request.POST.get('txtPrecioB')
                numeroInmubleTipoC = int(request.POST.get('txtNumtipoC'))
                precioTipoC = request.POST.get('txtPrecioC')
                numeroInmueblePenthouse = int(request.POST.get('txtNumTipoPenthouse'))
                precioTipoPenthouse = request.POST.get('txtPrecioPenthouse')
                foto_base64 = request.session.get('fotoProyecto', None)
                fotoProyecto = None  # Inicializar con valor None
                if foto_base64:
                    foto_bytes = base64.b64decode(foto_base64)
                    fotoProyecto = ContentFile(foto_bytes, name='foto_proyecto.jpg')
                with transaction.atomic():
                    #Guardamos la ubicacion del proyecto
                    ubicacion = Ubicacion(ubiDepartamento=departamento,
                                          ubiCuidad=ciudad,
                                          ubiDireccion=direccion)
                    ubicacion.save()
                    #guardamos el proyecto
                    proyecto = Proyecto(proNombre=nombreProyecto,
                                        proDescripcion=descripcion,
                                        proFiducia=fiducia,
                                        proFoto=fotoProyecto,
                                        proNumeroManzanasTorres=numeroTorresOManzanas,
                                        proNumeroInmuebles=numeroApartamentosOCasas,
                                        proNumeroDePisos=numeroPisos,
                                        proTotalInmuebles=totalInmuebles,
                                        proParqueadero=parqueadero,
                                        proUbicacion=ubicacion)
                    proyecto.save()
                    #creamos 3 objetos casas segun su tipo
                    apartametoA = Apartamento(
                                        apaNumeroHabitaciones=numeroHabitaciones,
                                        apaAreaConstruida=areaConstruida,
                                        apaCategoria="Tipo A",
                                        apaPrecioVivienda=precioTipoA)
                    apartametoA.save()
                    apartamentoB = Apartamento(
                                        apaNumeroHabitaciones=numeroHabitaciones,
                                        apaAreaConstruida=areaConstruida,
                                        apaCategoria="Tipo B",
                                        apaPrecioVivienda=precioTipoB)
                    apartamentoB.save()
                    apartamentoC = Apartamento(
                                        apaNumeroHabitaciones=numeroHabitaciones,
                                        apaAreaConstruida=areaConstruida,
                                        apaCategoria="Tipo C",
                                        apaPrecioVivienda=precioTipoC)
                    apartamentoC.save()
                    apartamentoPenthouse = Apartamento(
                        apaNumeroHabitaciones=numeroHabitaciones,
                        apaAreaConstruida=areaConstruida,
                        apaCategoria="Tipo penthouse",
                        apaPrecioVivienda=precioTipoPenthouse
                    )
                    apartamentoPenthouse.save()
                    #creamos los inmubles segun el numero de su tipo
                    for i in range(numeroInmubleTipoA):
                        inmueble = Inmueble(inmEntregaDeObra=obraEntregable,
                                            inmEstado="Disponible",
                                            inmApartamento=apartametoA,
                                            inmProyecto=proyecto)
                        inmueble.save()
                    for i in range(numeroInmubleTipoB):
                        inmueble = Inmueble(inmEntregaDeObra=obraEntregable,
                                            inmEstado="Disponible",
                                            inmApartamento=apartamentoB,
                                            inmProyecto=proyecto)
                        inmueble.save()
                    for i in range(numeroInmubleTipoC):
                        inmueble = Inmueble(inmEntregaDeObra=obraEntregable,
                                            inmEstado="Disponible",
                                            inmApartamento=apartamentoC,
                                            inmProyecto=proyecto)
                        inmueble.save()
                    for i in range(numeroInmueblePenthouse):
                        inmueble = Inmueble(inmEntregaDeObra=obraEntregable,
                                            inmEstado="Disponible",
                                            inmApartamento=apartamentoPenthouse,
                                            inmProyecto=proyecto)
                        inmueble.save()
                    #guardamos la fotos del inmueble que pertenencen al proyecto creado
                    for foto in fotosInmuble:
                        fotoInm = fotoInmuble(fotInmuble=foto,fotProyecto=proyecto)
                        fotoInm.save()
                    mensaje="Proyecto Registrado Exitosamente" 
                    retorno = {"mensaje":mensaje,"estado":True,"titulo":"Registro de Proyecto"} 
                    return render(request, 'administrador/inicioAdministrador.html',retorno)
        except Exception as error:
            transaction.rollback()
            mensaje = f"{error}"
        retorno = {"mensaje":mensaje,"estado":False}
        return render(request, 'administrador/registrarCasaoApartamento.html',retorno)
    

def listarProyectos(request):
    try:
        proyectos = []
        proyects = Proyecto.objects.all()
        for proyect in proyects:
            inmueble = Inmueble.objects.filter(inmProyecto=proyect.id).first()
            if inmueble.inmCasa:
                proyecto = {
                    'id': proyect.id,
                    'nombre': proyect.proNombre,
                    'ubicacion':proyect.proUbicacion.ubiDepartamento +","+proyect.proUbicacion.ubiCuidad,
                    'descripcion':proyect.proDescripcion,
                    'foto':str(proyect.proFoto),
                    'precio':inmueble.inmCasa.casPrecioVivienda,
                    'fecha':proyect.profechaHoraCreacion,
                    'fiducia':proyect.proFiducia,
                    'totalinmuebles':proyect.proTotalInmuebles,
                }
            else:
                proyecto = {
                    'id':proyect.id,
                    'nombre': proyect.proNombre,
                    'ubicacion':proyect.proUbicacion.ubiDepartamento +","+proyect.proUbicacion.ubiCuidad,
                    'descripcion':proyect.proDescripcion,
                    'foto':str(proyect.proFoto),
                    'precio':inmueble.inmApartamento.apaPrecioVivienda,
                    'fecha':proyect.profechaHoraCreacion,
                    'fiducia':proyect.proFiducia,
                    'totalinmuebles':proyect.proTotalInmuebles,
                }
            proyectos.append(proyecto)
        retorno = {'proyectos':proyectos}
        return JsonResponse(retorno)
    except Error as error:
        mensaje=f"{error}"
        return JsonResponse(mensaje)
    
def buscarProyecto(request, id):
    try:
        proyect = Proyecto.objects.filter(id=id).first()

        proyecto = {
            'id': proyect.id,
            'nombre': proyect.proNombre,
            'fiducia':proyect.proFiducia,
            'departamento': proyect.proUbicacion.ubiDepartamento,
            'municipio': proyect.proUbicacion.ubiCuidad,
            'descripcion': proyect.proDescripcion,
            'parqueadero': proyect.proParqueadero,
            'foto': str(proyect.proFoto),
            'direccion': proyect.proUbicacion.ubiDireccion
        }
        
        retorno = {'proyecto': proyecto}
        return JsonResponse(retorno)  # Return JSON response instead of rendering HTML
    except Error as error:
        mensaje = f"{error}"
        return JsonResponse({'mensaje': mensaje}, status=500)  # Return JSON response with error message
    
    
def proyectosCarrusel(request):
    try:
        proyectos = []
        proyects = Proyecto.objects.order_by('-profechaHoraCreacion')[:5]
        for proyect in proyects:
            proyecto = {
                'nombre':proyect.proNombre,
                'foto':str(proyect.proFoto),
                'ubicacion':proyect.proUbicacion.ubiDepartamento +","+proyect.proUbicacion.ubiCuidad,
            }
            proyectos.append(proyecto)
        retorno = {'proyectos':proyectos}
        return JsonResponse(retorno)
    except Exception as error:
        mensaje={'error':error}
        return JsonResponse(mensaje)
    
def proyectoDetalleCarrusel(request, id):
    try:
        fotosInmuebles = []
        fotosInm = fotoInmuble.objects.filter(fotProyecto=id)
        for fotoinm in fotosInm:
            proyectoDetal ={
                'imagen': str(fotoinm.fotInmuble)
            }
            fotosInmuebles.append(proyectoDetal)
        retorno = {'imagenes':fotosInmuebles}
        return JsonResponse(retorno)
    except Exception as error:
        mensaje={'error':error}
        return  JsonResponse(mensaje)
    
    


def modificarProyecto(request, id):
    if request.method == 'POST':
        try:
                nombreProyecto = request.POST["txtNombreProyecto"]
                fiducia = request.POST["cbFiducia"]
                parqueadero = request.POST["cbParqueadero"]
                foto = request.FILES.get("fileFoto", False)
                direccion = request.POST["txtDireccion"]
                descripcion = request.POST["txtDescripcion"]
                departamento = request.POST["cbDepartamento"]
                municipio = request.POST["cbMunicipio"]
                with transaction.atomic():
                    proyecto=Proyecto.objects.get(pk=id)
                    proyecto.proNombre = nombreProyecto
                    proyecto.proFiducia = fiducia
                    proyecto.proParqueadero = parqueadero
                    proyecto.proDescripcion = descripcion
                    if(foto):
                        os.remove('./media/'+str(proyecto.proFoto))
                        proyecto.proFoto = foto
                    proyecto.save()
                    ubicacion=Ubicacion.objects.get(pk=proyecto.proUbicacion.id)
                    ubicacion.ubiDireccion=direccion
                    if(departamento and municipio):
                        ubicacion.ubiDepartamento=departamento
                        ubicacion.ubiCuidad=municipio
                    ubicacion.save()
                    mensaje = "Datos Modificados Correctamente"
                    retorno = {"mensaje": mensaje,"estado":True}
                    return render(request, 'administrador/modificarProyectos.html',retorno)
        except Error as error:
            transaction.rollback()
            mensaje = f"{error}"
            retorno = {"mensaje":mensaje,"estado":False}
        return render(request, 'administrador/modificarProyectos.html',retorno)



    
    
    
        