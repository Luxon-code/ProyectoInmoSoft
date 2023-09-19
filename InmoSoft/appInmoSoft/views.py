from datetime import date, datetime
from django.shortcuts import render, redirect
from appInmoSoft.models import *
from appInmoSoft.serializers import *
from rest_framework import generics
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
        retorno = {"user":request.user,'entregaObra':entregaDeObra,'parqueaderos':tipoDeParqueadero, 'fiducia':fiducia,
                   'tipoProyecto':tipoDeProyecto}  
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
    
def vistaDetalleProyecto(request, proyecto_id):
        proyect = Proyecto.objects.filter(id=proyecto_id).first()
        inmueble = Inmueble.objects.filter(inmProyecto=proyect.id).first()
        
        if inmueble.inmCasa:
                proyecto = {
                    'id': proyect.id,
                    'nombre': proyect.proNombre,
                    'costoSeparacion':f"{proyect.proCostoSeparacion:,}",
                    'ubicacion':proyect.proUbicacion.ubiDepartamento +","+proyect.proUbicacion.ubiCuidad,
                    'descripcion':proyect.proDescripcion,
                    'parqueadero':proyect.proParqueadero,
                    'areaConstruida':inmueble.inmCasa.casAreaConstruida,
                    'foto':proyect.proFoto,
                    'precio':f"{inmueble.inmCasa.casPrecioVivienda:,}",
                    'numInmuebles':proyect.proTotalInmuebles,
                    'numdivision':proyect.proNumeroManzanasTorres,
                    'tipo':proyect.proTipo,
                    'division':"Manzanas",
                }
        else:
                proyecto = {
                    'id':proyect.id,
                    'nombre': proyect.proNombre,
                    'costoSeparacion':f"{proyect.proCostoSeparacion:,}",
                    'ubicacion':proyect.proUbicacion.ubiDepartamento +","+proyect.proUbicacion.ubiCuidad,
                    'descripcion':proyect.proDescripcion,
                    'parqueadero':proyect.proParqueadero,
                    'areaConstruida':inmueble.inmApartamento.apaAreaConstruida,
                    'foto':proyect.proFoto,
                    'precio':f"{inmueble.inmApartamento.apaPrecioVivienda:,}",
                    'numInmuebles':proyect.proTotalInmuebles,
                    'numdivision':proyect.proNumeroManzanasTorres,
                    'tipo':proyect.proTipo,
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
        retorno = {"user":request.user,'entregaObra':entregaDeObra,'parqueaderos':tipoDeParqueadero, 'fiducia':fiducia,
                   'tipos':tipoDeProyecto}  
        return render(request,'administrador/modificarProyectos.html',retorno)
    else:
        mensaje = "Debe iniciar sesión"
        return render(request,'inicioSesion.html',{"mensaje":mensaje})

@soloAsesor   
def vistaImmueblesDisponibles(request, id):
    if request.user.is_authenticated:
        retorno = {"user":request.user,'idProyecto':id}  
        return render(request,'asesor/listaInmueblesDisponibles.html',retorno)
    else:
        mensaje = "Debe iniciar sesión"
        return render(request,'inicioSesion.html',{"mensaje":mensaje})

@soloAsesor  
def vistaSepararInmueble(request,id):
    if request.user.is_authenticated:
        hoy = date.today()
        inmueble = Inmueble.objects.get(pk=id)
        if inmueble.inmCasa:
            inmu = {
                'id':inmueble.id,
                'hoy': hoy.strftime("%Y-%m-%d"),
                'precioMostrar':f"{inmueble.inmCasa.casPrecioVivienda:,}",
                'precio':inmueble.inmCasa.casPrecioVivienda,
                'costoSeparacion':inmueble.inmProyecto.proCostoSeparacion
            }
        else:
            inmu = {
                'id':inmueble.id,
                'hoy': hoy.strftime("%Y-%m-%d"),
                'precioMostrar':f"{inmueble.inmApartamento.apaPrecioVivienda:,}",
                'precio':inmueble.inmApartamento.apaPrecioVivienda,
                'costoSeparacion':inmueble.inmProyecto.proCostoSeparacion
            }
        retorno = {"user":request.user, 'inmueble':inmu}  
        return render(request,'asesor/separarInmueble.html',retorno)  
    else:
        mensaje = "Debe iniciar sesión"
        return render(request,'inicioSesion.html',{"mensaje":mensaje})    
#-------------------------------------FUNCIONES--------------------------#       

def registrarUsuario(request):
    """
    Registra un nuevo usuario en el sistema.

    Args:
        request (HttpRequest): La solicitud HTTP que contiene la información del usuario a registrar.

    Returns:
        HttpResponse: Una respuesta HTTP que generalmente redirige al usuario a una página de registro o muestra un mensaje de éxito o error.
    """
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
                https://inmosoft.pythonanywhere.com'
            thread = threading.Thread(
                target=enviarCorreo, args=(asunto, mensajeCorreo, [user.email]))
            thread.start()
            return render(request, 'administrador/registrarUsuario.html',retorno)
    except Exception as error:
        transaction.rollback()
        if 'userCedula' in str(error):
            mensaje = "Ya existe un usuario con esta cedula"
        elif 'user.username' in str(error):
            mensaje = "Ya existe un usuario con este correo electronico"
        elif 'user.email' in str(error):
            mensaje = "Ya existe un usuario con este correo electronico"
        else:
            mensaje = error
    retorno = {"mensaje": mensaje,"estado":False,'roles':Group.objects.all(),
                "cedula" : cedula,"nombres" : nombres,"apellidos" : apellidos,
                "correo" : correo,"telefono" : telefono
                }
    return render(request, "administrador/registrarUsuario.html",retorno)

def enviarCorreo(asunto=None, mensaje=None, destinatario=None,archivo=None):
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
            asunto, mensaje, remitente, destinatario)
        correo.attach_alternative(contenido, 'text/html')
        if archivo != None:
            correo.attach_file(archivo)
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
    """
    Obtiene la lista de usuarios registrados en el sistema y devuelve una respuesta JSON con la información.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.

    Returns:
        JsonResponse: Una respuesta JSON que contiene la lista de usuarios en formato de diccionario.
                      En caso de error, la respuesta contendrá un mensaje de error.
    """
    try:
        retorno = {
            "usuarios":list(User.objects.all().values()),
        }
        return JsonResponse(retorno)
    except Error as error:
        mensaje=f"{error}"
        
def cambiarEstadoUsuario(request,id):
    """
    Cambia el estado (activo/inactivo) de un usuario en el sistema y devuelve una respuesta JSON con el resultado.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        id (int): El ID del usuario cuyo estado se desea cambiar.

    Returns:
        JsonResponse: Una respuesta JSON que indica si el cambio de estado fue exitoso y contiene un mensaje correspondiente.
    """
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
    """
    Maneja el inicio de sesión de usuarios en el sistema.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.

    Returns:
        HttpResponse: Una respuesta HTTP que redirige al usuario a la página de inicio correspondiente o muestra un mensaje de error.
    """
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
    """
    Maneja el inicio de sesión de usuarios a través de una API.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        usuario (str): El nombre de usuario proporcionado para iniciar sesión.
        contraseña (str): La contraseña proporcionada para iniciar sesión.

    Returns:
        JsonResponse: Una respuesta JSON que indica si el inicio de sesión fue exitoso y contiene información del usuario o un mensaje de error.
    """
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
                                'foto':str(request.user.userFoto),'idUser':request.user.id})
        else:
            return JsonResponse({'mensaje':'Inicio de sesión exitoso como asesor','estado':True,'username':request.user.username,
                                'correo':request.user.email,'nombre':request.user.first_name,'apellidos':request.user.last_name,
                                'foto':str(request.user.userFoto),'idUser':request.user.id})
    else:
        mensaje = "El Usuario o Contraseña Son Incorrectas"
        return JsonResponse({'mensaje':mensaje,'estado':False,'username':"",
                                'correo':"",'nombre':"",'apellidos':"",
                                'foto':"",'idUser':""})

def cerrarSesion(request):
    """
    Cierra la sesión de usuario en el sistema y redirige a la página de inicio de sesión.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.

    Returns:
        HttpResponse: Una respuesta HTTP que redirige al usuario a la página de inicio de sesión con un mensaje de confirmación.
    """
    auth.logout(request)
    return render(request, "inicioSesion.html",
                  {"mensaje": "Ha cerrado la sesión"})
    
def modificarDatosUserPerfil(request,id):
    """
    Modifica los datos de un usuario en su perfil y guarda los cambios en la base de datos.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        id (int): El ID del usuario cuyos datos se desean modificar.

    Returns:
        HttpResponse: Una respuesta HTTP que redirige al perfil del usuario con un mensaje de éxito o error.
    """
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
    """
    Cambia la contraseña de un usuario y guarda los cambios en la base de datos.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        id (int): El ID del usuario cuya contraseña se desea cambiar.

    Returns:
        HttpResponse: Una respuesta HTTP que redirige al perfil del usuario con un mensaje de éxito o error.
    """
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
    """
    Recopila y almacena los datos del primer formulario de registro de proyecto en la sesión del usuario.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.

    Returns:
        HttpResponse: Una respuesta HTTP que redirige al usuario a la siguiente etapa del registro del proyecto.
    """
    datosForm1 = {
        'nombreProyecto': request.POST.get('txtNombreProyecto'),
        'tipoProyecto': request.POST.get('cbTipoProyecto'),
        'fiducia': request.POST.get('cbFiducia'),
        'costoSeparacion': request.POST.get('txtCostSeparacion'),
        'numeroTorresOManzanas': int(request.POST.get('txtNumeroTorresoManzanas')),
        'numeroApartamentosOCasas': int(request.POST.get('txtNumerosApartamentosoCasas')),
        'numeroPisos':int(request.POST.get('txtPisos')),
        'totalInmuebles': int(request.POST.get('txtTotalInmuebles')),
        'obraEntregable': request.POST.get('cbObraentregable'),
        'parqueadero': request.POST.get('cbParqueadero'),
        'cantidaParqueaderos': request.POST.get('txtCantParqueadero'),
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
    """
    Registra un proyecto en la base de datos, incluyendo sus detalles y tipos de inmuebles asociados.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.

    Returns:
        HttpResponse: Una respuesta HTTP que redirige al usuario a la página de inicio del administrador con un mensaje de éxito o error.
    """
    
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
                tipoProyecto = request.POST.get('cbTipoProyecto')
                numeroHabitaciones=request.POST.get('txtNumHabitaciones')
                areaConstruida=request.POST.get('txtAreaConstruida')
                fotosInmuble = request.FILES.getlist('fileFotosCasa')
                numeroInmubleTipoA = request.POST.get('txtNumtipoA')
                precioTipoA = request.POST.get('txtPrecioA')
                numeroInmubleTipoB = request.POST.get('txtNumtipoB')
                precioTipoB = request.POST.get('txtPrecioB')
                numeroInmubleTipoC = request.POST.get('txtNumtipoC')
                precioTipoC = request.POST.get('txtPrecioC')
                foto_base64 = request.session.get('fotoProyecto', None)
                fotoProyecto = None # Inicializar con valor None
                costoSeparacion= request.POST.get('txtCostSeparacion')
                cantidadParqueaderos = request.POST.get('txtCantParqueadero')
                
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
                                        proUbicacion=ubicacion,
                                        proTipo=tipoProyecto,
                                        proCostoSeparacion=costoSeparacion,
                                        proCantidadParqueadero=cantidadParqueaderos)
                    proyecto.save()
                    #creamos 3 objetos casas segun su tipo
                    if precioTipoA:
                        casaA = Casas(casNumeroHabitaciones=numeroHabitaciones,
                                            casAreaConstruida=areaConstruida,
                                            casCategoria="Tipo A",
                                            casPrecioVivienda=precioTipoA)
                        casaA.save()
                    if precioTipoB:
                        casaB = Casas(casNumeroHabitaciones=numeroHabitaciones,
                                            casAreaConstruida=areaConstruida,
                                            casCategoria="Tipo B",
                                            casPrecioVivienda=precioTipoB)
                        casaB.save()
                    if precioTipoC:
                        casaC = Casas(casNumeroHabitaciones=numeroHabitaciones,
                                            casAreaConstruida=areaConstruida,
                                            casCategoria="Tipo C",
                                            casPrecioVivienda=precioTipoC)
                        casaC.save()
                    #creamos los inmubles segun el numero de su tipo
                    if numeroInmubleTipoA:
                        for i in range(int(numeroInmubleTipoA)):
                            inmueble = Inmueble(inmEntregaDeObra=obraEntregable,
                                                inmEstado="Disponible",
                                                inmCasa=casaA,
                                                inmProyecto=proyecto)
                            inmueble.save()
                    if numeroInmubleTipoB:
                        for i in range(int(numeroInmubleTipoB)):
                            inmueble = Inmueble(inmEntregaDeObra=obraEntregable,
                                                inmEstado="Disponible",
                                                inmCasa=casaB,
                                                inmProyecto=proyecto)
                            inmueble.save()
                    if numeroInmubleTipoC: 
                        for i in range(int(numeroInmubleTipoC)):
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
                costoSeparacion= request.POST.get('txtCostSeparacion')
                cantidadParqueaderos = request.POST.get('txtCantParqueadero')
                tipoProyecto = request.POST.get('cbTipoProyecto')
                numeroHabitaciones=request.POST.get('txtNumHabitaciones')
                areaConstruida=request.POST.get('txtAreaConstruida')
                fotosInmuble = request.FILES.getlist('fileFotosApartamento')
                numeroInmubleTipoA = request.POST.get('txtNumtipoA')
                precioTipoA = request.POST.get('txtPrecioA')
                numeroInmubleTipoB = request.POST.get('txtNumtipoB')
                precioTipoB = request.POST.get('txtPrecioB')
                numeroInmubleTipoC = request.POST.get('txtNumtipoC')
                precioTipoC = request.POST.get('txtPrecioC')
                numeroInmueblePenthouse = request.POST.get('txtNumTipoPenthouse')
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
                                        proUbicacion=ubicacion,
                                        proTipo=tipoProyecto,
                                        proCostoSeparacion=costoSeparacion,
                                        proCantidadParqueadero=cantidadParqueaderos)
                    proyecto.save()
                    #creamos 3 objetos apartamento segun su tipo
                    if precioTipoA:
                        apartametoA = Apartamento(
                                            apaNumeroHabitaciones=numeroHabitaciones,
                                            apaAreaConstruida=areaConstruida,
                                            apaCategoria="Tipo A",
                                            apaPrecioVivienda=precioTipoA)
                        apartametoA.save()
                    if precioTipoB:
                        apartamentoB = Apartamento(
                                            apaNumeroHabitaciones=numeroHabitaciones,
                                            apaAreaConstruida=areaConstruida,
                                            apaCategoria="Tipo B",
                                            apaPrecioVivienda=precioTipoB)
                        apartamentoB.save()
                    if precioTipoC:
                        apartamentoC = Apartamento(
                                            apaNumeroHabitaciones=numeroHabitaciones,
                                            apaAreaConstruida=areaConstruida,
                                            apaCategoria="Tipo C",
                                            apaPrecioVivienda=precioTipoC)
                        apartamentoC.save()
                    if precioTipoPenthouse:
                        apartamentoPenthouse = Apartamento(
                            apaNumeroHabitaciones=numeroHabitaciones,
                            apaAreaConstruida=areaConstruida,
                            apaCategoria="Tipo penthouse",
                            apaPrecioVivienda=precioTipoPenthouse
                        )
                        apartamentoPenthouse.save()
                    #creamos los inmubles segun el numero de su tipo
                    if numeroInmubleTipoA:
                        for i in range(int(numeroInmubleTipoA)):
                            inmueble = Inmueble(inmEntregaDeObra=obraEntregable,
                                                inmEstado="Disponible",
                                                inmApartamento=apartametoA,
                                                inmProyecto=proyecto)
                            inmueble.save()
                    if numeroInmubleTipoB:
                        for i in range(int(numeroInmubleTipoB)):
                            inmueble = Inmueble(inmEntregaDeObra=obraEntregable,
                                                inmEstado="Disponible",
                                                inmApartamento=apartamentoB,
                                                inmProyecto=proyecto)
                            inmueble.save()
                    if numeroInmubleTipoC:
                        for i in range(int(numeroInmubleTipoC)):
                            inmueble = Inmueble(inmEntregaDeObra=obraEntregable,
                                                inmEstado="Disponible",
                                                inmApartamento=apartamentoC,
                                                inmProyecto=proyecto)
                            inmueble.save()
                    if numeroInmueblePenthouse:
                        for i in range(int(numeroInmueblePenthouse)):
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
    """
    Recupera y lista los proyectos disponibles junto con sus detalles, incluyendo su tipo, ubicación, descripción, foto, precio,
    fecha de creación, fiducia y total de inmuebles disponibles.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.

    Returns:
        JsonResponse: Una respuesta JSON que contiene una lista de proyectos y sus detalles.
    """
    try:
        proyectos = []
        proyects = Proyecto.objects.filter(proEstado=True).all()
        for proyect in proyects:
            inmueble = Inmueble.objects.filter(inmProyecto=proyect.id).first()
            if inmueble.inmCasa:
                proyecto = {
                    'id': proyect.id,
                    'nombre': proyect.proNombre,
                    'tipo':proyect.proTipo,
                    'ubicacion':proyect.proUbicacion.ubiDepartamento +","+proyect.proUbicacion.ubiCuidad,
                    'descripcion':proyect.proDescripcion,
                    'foto':str(proyect.proFoto),
                    'precio':f"{inmueble.inmCasa.casPrecioVivienda:,}",
                    'fecha':proyect.profechaHoraCreacion,
                    'fiducia':proyect.proFiducia,
                    'totalinmuebles':proyect.proTotalInmuebles,
                }
            else:
                proyecto = {
                    'id':proyect.id,
                    'tipo':proyect.proTipo,
                    'nombre': proyect.proNombre,
                    'ubicacion':proyect.proUbicacion.ubiDepartamento +","+proyect.proUbicacion.ubiCuidad,
                    'descripcion':proyect.proDescripcion,
                    'foto':str(proyect.proFoto),
                    'precio':f"{inmueble.inmApartamento.apaPrecioVivienda:,}",
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
    
def listarInmuebles(request,id):
    """
    Lista los inmuebles disponibles de un proyecto específico junto con sus detalles, incluyendo el precio, tipo y disponibilidad.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        id (int): El ID del proyecto del cual se listarán los inmuebles.

    Returns:
        JsonResponse: Una respuesta JSON que contiene una lista de inmuebles y sus detalles.
    """
    try:
        inmuebles=[]
        inmuebless= Inmueble.objects.filter(inmProyecto= id,inmEstado='Disponible')
        for inmuebl in inmuebless:
            if inmuebl.inmCasa:
                inmueble={
                    'id': inmuebl.id,
                    'Precio':inmuebl.inmCasa.casPrecioVivienda,
                    'tipo':inmuebl.inmCasa.casCategoria,
                    'disponibilidad':inmuebl.inmEstado,
                }
            else:
                inmueble={
                    'id': inmuebl.id,
                    'Precio':inmuebl.inmApartamento.apaPrecioVivienda,
                    'tipo':inmuebl.inmApartamento.apaCategoria,
                    'disponibilidad':inmuebl.inmEstado,
                }
            inmuebles.append(inmueble)
        retorno ={'inmuebles':inmuebles}
        return JsonResponse(retorno)
    except Error as error:
        mensaje=f"{error}"
        return JsonResponse(mensaje)	
               
def buscarProyecto(request, id):
    """
    Busca y devuelve los detalles de un proyecto específico por su ID.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        id (int): El ID del proyecto que se desea buscar.

    Returns:
        JsonResponse: Una respuesta JSON que contiene los detalles del proyecto encontrado.
    """
    try:
        proyect = Proyecto.objects.filter(id=id).first()

        proyecto = {
            'id': proyect.id,
            'nombre': proyect.proNombre,
            'fiducia':proyect.proFiducia,
            'tipo':proyect.proTipo,
            'costoSeparacion':proyect.proCostoSeparacion,
            'cantParquedero':proyect.proCantidadParqueadero,
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
    """
    Obtiene los últimos 5 proyectos activos y devuelve sus detalles para mostrar en un carrusel.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.

    Returns:
        JsonResponse: Una respuesta JSON que contiene los detalles de los proyectos para el carrusel.
    """
    try:
        proyectos = []
        proyects = Proyecto.objects.filter(proEstado=True).order_by('-profechaHoraCreacion')[:5]
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
    """
    Obtiene las fotos de los inmuebles asociados a un proyecto específico para mostrar en un carrusel.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        id (int): El identificador único del proyecto del cual se obtendrán las fotos.

    Returns:
        JsonResponse: Una respuesta JSON que contiene las fotos de los inmuebles asociados al proyecto.
    """
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
    """
    Modifica los datos de un proyecto existente en la base de datos.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        id (int): El identificador único del proyecto que se desea modificar.

    Returns:
        HttpResponse: Una respuesta HTTP que indica si la modificación fue exitosa o si se produjo un error.
    """
    if request.method == 'POST':
        try:
                nombreProyecto = request.POST["txtNombreProyecto"]
                fiducia = request.POST["cbFiducia"]
                tipo = request.POST["cbTipo"]
                costoSeparacion = request.POST["txtCostoSeparacion"]
                cantParquederos = request.POST["txtCantParqueadero"]
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
                    proyecto.proTipo = tipo
                    proyecto.proCostoSeparacion = costoSeparacion
                    proyecto.proCantidadParqueadero = cantParquederos
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
    
def enviarCotizacion(request,id):
    """
    Esta función maneja la lógica para enviar una cotización por correo electrónico y realizar otras tareas relacionadas.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        id (int): El ID del proyecto.

    Returns:
        HttpResponse: Una respuesta HTTP que indica si el envio fue exitoso o si se produjo un error.
    """
    if request.method == 'POST':
        try:
            proyect = Proyecto.objects.get(pk=id)
            inmueble = Inmueble.objects.get(pk=proyect.id)
            datos = {
                'cedula': request.POST.get('txtCedula'),
                'nombre': request.POST.get('txtNombre'),
                'apellido': request.POST.get('txtApellido'),
                'celular': request.POST.get('txtCelular'),
                'correo': request.POST.get('txtCorreo'),
                'nombreProyecto': proyect.proNombre,
                'fiducia': proyect.proFiducia,
                'tipo': proyect.proTipo,
                'costoSeparacion': proyect.proCostoSeparacion,
                'cantParquedero': proyect.proCantidadParqueadero,
                'departamento': proyect.proUbicacion.ubiDepartamento,
                'municipio': proyect.proUbicacion.ubiCuidad,
                'descripcion': proyect.proDescripcion,
                'parqueadero': proyect.proParqueadero,
                'foto': str(proyect.proFoto),
                'precio': inmueble.inmCasa.casPrecioVivienda if inmueble.inmCasa else inmueble.inmApartamento.apaPrecioVivienda,
                'direccion': proyect.proUbicacion.ubiDireccion
            }
            archivo = generarPdfCotizacion(datos)
            # enviar correo al usuario
            asunto = 'Cotizacion Sistema InmoSoft'
            mensajeCorreo = f'Cordial saludo, <b>{datos["nombre"]} {datos["apellido"]}</b>, nos permitimos.\
                informarle que usted ha pedido la cotizacion de un proyecto en nuestro Sistema Inmosoft de la ciudad de Neiva-Huila\
                por lo tanto, en lo mas pronto posible uno de nuestros asesores se comunicara con usted.<br>\
                Nos permitimos enviarle un pdf adjunto sobre su cotizacion.<br>\
                <br><br>Para cualquier duda lo invitamos a ingresar a nuestro sistema en la url:\
                https://inmosoft.pythonanywhere.com'
            thread = threading.Thread(
                target=enviarCorreo, args=(asunto, mensajeCorreo, [datos['correo']],archivo))
            thread.start()
            usuarios = User.objects.filter(userTipo='Asesor')
            for usuario in usuarios:
                asunto = 'Cotizacion Sistema InmoSoft'
                mensajeCorreo = f'Cordial saludo, <b>{usuario.first_name} {usuario.last_name}</b>, nos permitimos.\
                informarle que la persona {datos["nombre"]} {datos["apellido"]} ha pedido la cotizacion de un proyecto en nuestro Sistema Inmosoft de la ciudad de Neiva-Huila\
                por lo tanto, en lo mas pronto posible le pedimos que se comunique con el para generar una posible venta.<br>\
                Nos permitimos enviarle un pdf adjunto con los datos de la persona y el proyecto interesado.<br>\
                <br><br>Para cualquier duda lo invitamos a ingresar a nuestro sistema en la url:\
                https://inmosoft.pythonanywhere.com'
                thread = threading.Thread(
                    target=enviarCorreo, args=(asunto, mensajeCorreo, [usuario.email],archivo))
                thread.start()
            mensaje = "Se le enviado un correo electronico a su correo con la informacion de su cotizacion"
            retorno= {"mensaje":mensaje,"estado":True,"id":proyect.id}
            return render(request,'detalleInmueble.html',retorno)
        except Error as error:
            mensaje = f"{error}"
            retorno = {"mensaje":mensaje,"estado":False,"id":proyect.id}
            return render(request,'detalleInmueble.html',retorno)
            
            
def generarPdfCotizacion(datos):
    """
    Esta función genera un archivo PDF de cotización utilizando la clase PdfCotizacion personalizada.

    Args:
        datos (dict): Un diccionario que contiene los datos de cotización a incluir en el PDF.

    Returns:
        str: La ruta del archivo PDF generado.
    """
    from appInmoSoft.pdfCotizacion import PdfCotizacion
    pdf = PdfCotizacion()
    pdf.add_page()
    pdf.mostrarDatos(datos)
    pdf.output(f'media/cotizacion.pdf','F')
    return "media/cotizacion.pdf"


def separarInmueble(request,id):
    if request.method == 'POST':
        try:
            #Datos del cliente
            nombre = request.POST.get('txtNombre')
            apellido = request.POST.get('txtApellido')
            cedula = request.POST.get('txtCedula')
            telefono = request.POST.get('txtTelefono')
            direccion = request.POST.get('txtDireccion')
            correo = request.POST.get('txtCorreo')
            estadoCivil = request.POST.get('cbEstadoCivil')
            #datos del familiar o conyugue
            nombreFamiliar = request.POST.get('txtNombreFamiliar')
            apellidoFamiliar = request.POST.get('txtApellidoFamiliar')
            cedulaFamiliar = request.POST.get('txtCedulaFamiliar')
            telefonoFamiliar = request.POST.get('txtTelefonoFamiliar')
            direccionFamiliar = request.POST.get('txtDireccionFamiliar')
            correoFamiliar = request.POST.get('txtCorreoFamiliar')
            #datos del plan de pago
            numeroCuotas = request.POST.get('txtNumeroCuotas')
            fechaInicio = request.POST.get('fechaInicio')
            fechaFinal = request.POST.get('fechaFinal')
            fechaFinal = datetime.strptime(fechaFinal,"%d/%m/%Y")
            fechaFinal = fechaFinal.strftime("%Y-%m-%d")
            cuotaInicial = request.POST.get('cuotaInicial')
            valorCuota = request.POST.get('valorCuota')
            with transaction.atomic():
                if(nombreFamiliar and apellidoFamiliar and cedulaFamiliar
                   and telefonoFamiliar and direccionFamiliar and correoFamiliar):
                    familiar = Familiar(faNombre=nombreFamiliar,faApellido=apellidoFamiliar,
                                        faTelefono=telefonoFamiliar,faCorreo=correoFamiliar,
                                        faCedula=cedulaFamiliar,faDireccion=direccionFamiliar)
                    familiar.save()
                    cliente = Cliente(cliNombre=nombre,cliApellido=apellido,
                                  cliTelefono=telefono,cliCedula=cedula,cliCorreo=correo,
                                  cliDireccion=direccion,cliEstadoCivil=estadoCivil,cliFamiliar=familiar)
                    cliente.save()
                else:
                    cliente = Cliente(cliNombre=nombre,cliApellido=apellido,
                                  cliTelefono=telefono,cliCedula=cedula,cliCorreo=correo,
                                  cliDireccion=direccion,cliEstadoCivil=estadoCivil)
                    cliente.save()
                inmueble = Inmueble.objects.get(pk=id)
                inmueble.inmEstado = "Separado"
                inmueble.save()
                venta = Venta(venUsuario=request.user,venInmueble=inmueble,venCliente=cliente)
                venta.save()
                planPago = PlanDePago(plaFechaInicial=fechaInicio,plaFechaFinal=fechaFinal,
                                      plaNumCuota=numeroCuotas,plaCuotaInicial=cuotaInicial,
                                      plaValorDeCuota=valorCuota,plaVenta=venta)
                planPago.save()
                archivo = generarPdfSeparacion(planPago)
                # enviar correo al usuario
                asunto = 'Separacion de Inmueble Sistema InmoSoft'
                mensajeCorreo = f'Cordial saludo, <b>{cliente.cliNombre} {cliente.cliApellido}</b>, nos permitimos.\
                informarle que usted ha separado un inmueble de un proyecto en nuestro Sistema Inmosoft de la ciudad de Neiva-Huila\
                por lo tanto,Nos permitimos enviarle un pdf adjunto con toda la informacion sobre la separacion del inmueble incluyendo el plan de pago.<br>\
                <br><br>Para cualquier duda lo invitamos a ingresar a nuestro sistema en la url:\
                https://inmosoft.pythonanywhere.com'
                thread = threading.Thread(
                    target=enviarCorreo, args=(asunto, mensajeCorreo, [cliente.cliCorreo],archivo))
                thread.start()
                mensaje="Inmueble separado correctamente"
                retorno = {"mensaje":mensaje,"estado":True,'idProyecto':inmueble.inmProyecto.id}
                return render(request,"asesor/separarInmueble.html",retorno)
        except Exception as error:
            mensaje = f"{error}"
            retorno = {"mensaje":mensaje,"estado":False}
            return render(request,"asesor/separarInmueble.html",retorno)
        
def generarPdfSeparacion(planPago:PlanDePago):
    from appInmoSoft.pdfSeparacion import PdfSeparacion
    pdf = PdfSeparacion()
    pdf.add_page()
    pdf.mostrarDatos(planPago)
    pdf.output(f'media/separacion.pdf','F')
    return "media/separacion.pdf"


#-----------------------------/APIS/-----------------------------------------

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
