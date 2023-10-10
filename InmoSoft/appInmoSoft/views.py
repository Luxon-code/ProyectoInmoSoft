from datetime import date, datetime
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from appInmoSoft.models import *
from appInmoSoft.serializers import *
from rest_framework import generics
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt
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
from django.core.mail import EmailMessage
from django.template.loader import get_template
import threading
import requests
from smtplib import SMTPException
from django.http import JsonResponse
from django.db.models import Sum, Avg, Count
from datetime import datetime, timedelta
from django.db.models import Count
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
                    'direccion':proyect.proUbicacion.ubiDireccion,
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
                    'direccion':proyect.proUbicacion.ubiDireccion,
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
                'idProyecto':inmueble.inmProyecto.id,
                'hoy': hoy.strftime("%Y-%m-%d"),
                'precioMostrar':f"{inmueble.inmCasa.casPrecioVivienda:,}",
                'precio':inmueble.inmCasa.casPrecioVivienda,
                'costoSeparacion':inmueble.inmProyecto.proCostoSeparacion
            }
        else:
            inmu = {
                'id':inmueble.id,
                'idProyecto':inmueble.inmProyecto.id,
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
@soloAsesor 
def vistaListarVentasSeparadas(request):
    if request.user.is_authenticated:
        retorno = {"user":request.user}
        return render(request,'asesor/vistaListarVentasSeparadas.html',retorno)
    else:
        mensaje = "Debe iniciar sesión"
        return render(request,'inicioSesion.html',{"mensaje":mensaje})   
@soloAsesor 
def vistaListarVentasVendidas(request):
    if request.user.is_authenticated:
        retorno = {"user":request.user}
        return render(request,'asesor/vistaListarVentasVendidas.html',retorno)
    else:
        mensaje = "Debe iniciar sesión"
        return render(request,'inicioSesion.html',{"mensaje":mensaje})   
    
@soloAsesor
def vistaListaMora(request):
    if request.user.is_authenticated:
        retorno = {"user":request.user}
        return render(request,'asesor/vistaListaMora.html',retorno)
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

def enviarCorreo(asunto=None, mensaje=None, destinatario=None, archivo=None):
    remitente = settings.EMAIL_HOST_USER
    template = get_template('enviarCorreo.html')
    contenido = template.render({
        'destinatario': destinatario,
        'mensaje': mensaje,
        'asunto': asunto,
        'remitente': remitente,
    })
    try:
        correo = EmailMessage(
            asunto,
            contenido,  # Utilizamos el contenido HTML como el cuerpo del correo
            remitente,
            destinatario,
        )
        correo.content_subtype = "html"
        if archivo != None:
            correo.attach_file(archivo)
        correo.send(fail_silently=True)
    except Exception as error:
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
                verificarDesistimiento()
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
        proyects = Proyecto.objects.filter(proEstado=True).order_by('-profechaHoraCreacion').all()
        elementos_por_pagina = 2
        
        # Obtén el número de página actual desde la solicitud (por defecto es 1)
        pagina_actual = request.GET.get('page', 1)
        
        # Crea una instancia de Paginator
        paginator = Paginator(proyects, elementos_por_pagina)
        
        # Obtiene la página actual
        proyectos_pagina = paginator.get_page(pagina_actual)
        num_paginas = paginator.num_pages
        for proyect in proyectos_pagina:
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
        retorno = {'proyectos':proyectos,'num_paginas':num_paginas}
        return JsonResponse(retorno)
    except Error as error:
        mensaje=f"{error}"
        return JsonResponse(mensaje)
def listarProyectosModificar(request):
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
        proyects = Proyecto.objects.filter(proEstado=True).order_by('-profechaHoraCreacion').all()
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
        inmueble = Inmueble.objects.filter(inmProyecto=proyect.id).first()
        if inmueble.inmCasa:
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
                'direccion': proyect.proUbicacion.ubiDireccion,
                'precio':f"{inmueble.inmCasa.casPrecioVivienda:,}",
            }
        else:
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
                'direccion': proyect.proUbicacion.ubiDireccion,
                'precio':f"{inmueble.inmApartamento.apaPrecioVivienda:,}",
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
            clienteInteresado = ClienteInteresado(cliNombre=datos['nombre'],cliApellido=datos['apellido'],
                                                  cliTelefono=datos['celular'],cliCorreo=datos['correo'],
                                                  cliCedula=datos['cedula'],cliProyecto=proyect)
            clienteInteresado.save()
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
@csrf_exempt
def apiEnviarCotizacion(request,id):
    import json
    """
    Esta función maneja la lógica para enviar una cotización por correo electrónico y realizar otras tareas relacionadas.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        id (int): El ID del proyecto.

    Returns:
        HttpResponse: Una respuesta JSON que indica si el envio fue exitoso o si se produjo un error.
    """
    try:
        data = json.loads(request.body)
        proyect = Proyecto.objects.get(pk=id)
        inmueble = Inmueble.objects.get(pk=proyect.id)
        datos = {
            'cedula': data.get('txtCedula'),
            'nombre': data.get('txtNombre'),
            'apellido': data.get('txtApellido'),
            'celular': data.get('txtCelular'),
            'correo': data.get('txtCorreo'),
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
        clienteInteresado = ClienteInteresado(cliNombre=datos['nombre'],cliApellido=datos['apellido'],
                                              cliTelefono=datos['celular'],cliCorreo=datos['correo'],
                                              cliCedula=datos['cedula'],cliProyecto=proyect)
        clienteInteresado.save()
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
        return JsonResponse(retorno)
    except Error as error:
        mensaje = f"{error}"
        retorno = {"mensaje":mensaje,"estado":False,"id":proyect.id}
        return JsonResponse(retorno)
            
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

def separarInmueble(request, id):
    """
Esta función maneja la separación de un inmueble y realiza las siguientes acciones:
- Registra la información del cliente, incluyendo datos personales y familiares si se proporcionan.
- Cambia el estado del inmueble a "Separado".
- Crea una venta asociada al inmueble y al cliente con la fecha de separación especificada.
- Crea un plan de pago asociado a la venta.
- Genera un archivo PDF con detalles de la separación y lo envía por correo electrónico al cliente.
- Devuelve una respuesta HTTP con un mensaje de éxito o un mensaje de error.

Args:
    request (HttpRequest): La solicitud HTTP recibida.
    id (int): El ID del inmueble que se va a separar.

Returns:
    HttpResponse: Una respuesta HTTP que indica si la separación fue exitosa o si se produjo un error.
"""
    if request.method == 'POST':
        try:
            # Datos del cliente
            nombre = request.POST.get('txtNombre')
            apellido = request.POST.get('txtApellido')
            cedula = request.POST.get('txtCedula')
            telefono = request.POST.get('txtTelefono')
            direccion = request.POST.get('txtDireccion')
            correo = request.POST.get('txtCorreo')
            estadoCivil = request.POST.get('cbEstadoCivil')
            
            # Datos del familiar o cónyuge (si se proporcionan)
            nombreFamiliar = request.POST.get('txtNombreFamiliar')
            apellidoFamiliar = request.POST.get('txtApellidoFamiliar')
            cedulaFamiliar = request.POST.get('txtCedulaFamiliar')
            telefonoFamiliar = request.POST.get('txtTelefonoFamiliar')
            direccionFamiliar = request.POST.get('txtDireccionFamiliar')
            correoFamiliar = request.POST.get('txtCorreoFamiliar')
            
            # Datos del plan de pago
            numeroCuotas = request.POST.get('txtNumeroCuotas')
            fechaInicio = request.POST.get('fechaInicio')
            fechaFinal = request.POST.get('fechaFinal')
            fechaFinal = datetime.strptime(fechaFinal, "%d/%m/%Y")
            fechaFinal = fechaFinal.strftime("%Y-%m-%d")
            cuotaInicial = request.POST.get('cuotaInicial')
            valorCuota = request.POST.get('valorCuota')
            
            with transaction.atomic():
                if (nombreFamiliar and apellidoFamiliar and cedulaFamiliar
                   and telefonoFamiliar and direccionFamiliar and correoFamiliar):
                    # Registra un familiar si se proporcionan sus datos
                    familiar = Familiar(
                        faNombre=nombreFamiliar, faApellido=apellidoFamiliar,
                        faTelefono=telefonoFamiliar, faCorreo=correoFamiliar,
                        faCedula=cedulaFamiliar, faDireccion=direccionFamiliar
                    )
                    familiar.save()
                    
                    # Registra un cliente con datos del familiar
                    cliente = Cliente(
                        cliNombre=nombre, cliApellido=apellido,
                        cliTelefono=telefono, cliCedula=cedula, cliCorreo=correo,
                        cliDireccion=direccion, cliEstadoCivil=estadoCivil, cliFamiliar=familiar
                    )
                    cliente.save()
                else:
                    # Registra un cliente sin datos de familiar
                    cliente = Cliente(
                        cliNombre=nombre, cliApellido=apellido,
                        cliTelefono=telefono, cliCedula=cedula, cliCorreo=correo,
                        cliDireccion=direccion, cliEstadoCivil=estadoCivil
                    )
                    cliente.save()
                
                # Cambia el estado del inmueble a "Separado"
                inmueble = Inmueble.objects.get(pk=id)
                inmueble.inmEstado = "Separado"
                inmueble.save()
                
                # Crea una venta asociada al inmueble y al cliente con la fecha de separación especificada
                venta = Venta(venUsuario=request.user, venInmueble=inmueble, venCliente=cliente, venFechaSeparacion=fechaInicio)
                venta.save()
                
                # Crea un plan de pago asociado a la venta
                planPago = PlanDePago(
                    plaFechaInicial=fechaInicio, plaFechaFinal=fechaFinal,
                    plaNumCuota=numeroCuotas, plaCuotaInicial=cuotaInicial,
                    plaValorDeCuota=valorCuota, plaVenta=venta
                )
                planPago.save()
                
                # Genera un archivo PDF con detalles de la separación
                archivo = generarPdfSeparacion(planPago)
                
                # Envia correo electrónico al cliente con el archivo PDF adjunto
                asunto = 'Separacion de Inmueble Sistema InmoSoft'
                mensajeCorreo = f'Cordial saludo, <b>{cliente.cliNombre} {cliente.cliApellido}</b>, nos permitimos.\
                informarle que usted ha separado un inmueble de un proyecto en nuestro Sistema Inmosoft de la ciudad de Neiva-Huila.\
                Por lo tanto, nos permitimos enviarle un PDF adjunto con toda la información sobre la separación del inmueble, incluyendo el plan de pago.<br>\
                <br><br>Para cualquier duda lo invitamos a ingresar a nuestro sistema en la URL:\
                https://inmosoft.pythonanywhere.com'
                
                # Inicia un hilo para enviar el correo electrónico
                thread = threading.Thread(
                    target=enviarCorreo, args=(asunto, mensajeCorreo, [cliente.cliCorreo], archivo))
                thread.start()
                
                mensaje = "Inmueble separado correctamente"
                retorno = {"mensaje": mensaje, "estado": True, 'idProyecto': inmueble.inmProyecto.id}
                return render(request, "asesor/separarInmueble.html", retorno)
        except Exception as error:
            mensaje = f"{error}"
            retorno = {"mensaje": mensaje, "estado": False}
            return render(request, "asesor/separarInmueble.html", retorno)

        

def generarPdfSeparacion(planPago: PlanDePago):
    """
Esta función genera un archivo PDF que muestra los detalles de la separación de un inmueble en base a un plan de pago proporcionado.

Args:
    planPago (PlanDePago): El plan de pago asociado a la separación del inmueble.

Returns:
    str: La ruta al archivo PDF generado.
"""
    # Importa la clase PdfSeparacion desde el módulo pdfSeparacion
    from appInmoSoft.pdfSeparacion import PdfSeparacion
    # Crea una instancia de la clase PdfSeparacion
    pdf = PdfSeparacion()
    # Agrega una página al PDF
    pdf.add_page()
    # Muestra los datos del plan de pago en el PDF
    pdf.mostrarDatos(planPago)
    # Genera el archivo PDF y lo guarda en la ruta 'media/separacion.pdf'
    pdf.output(f'media/separacion.pdf', 'F')
    # Devuelve la ruta al archivo PDF generado
    return "media/separacion.pdf"



def ObtenerPlanPago(request, id):
    """
Esta función obtiene información sobre el plan de pago asociado a una venta específica y devuelve los datos en formato JSON.

Args:
    request (HttpRequest): La solicitud HTTP recibida.
    id (int): El ID de la venta para la cual se desea obtener el plan de pago.

Returns:
    HttpResponse: Una respuesta HTTP en formato JSON que contiene la información del plan de pago.
    En caso de error, se devuelve un mensaje de error con un código de estado HTTP 500.
"""
    # Obtiene el plan de pago asociado a la venta
    planpag = PlanDePago.objects.filter(plaVenta=id).first()
    
    # Obtiene la información del inmueble asociado a la venta
    inmueble = Venta.objects.filter(id=id).first()
    
    try:
        # Crea un diccionario 'planpago' con la información relevante del plan de pago
        planpago = {
            'idInmueble': inmueble.venInmueble.id,
            'idVenta': planpag.plaVenta.id,
            'fechaInicio': planpag.plaFechaInicial,
            'numCuotas': planpag.plaNumCuota,
            'valorCuotas': planpag.plaValorDeCuota,
            'valorCuotaInicial': planpag.plaCuotaInicial,
            'fechaFinal': planpag.plaFechaFinal
        }
        
        retorno = {'planpago': planpago}
        
        # Devuelve una respuesta JSON con la información del plan de pago.
        return JsonResponse(retorno)
    
    except Error as error:
        # En caso de error, devuelve un mensaje de error con un código de estado HTTP 500.
        mensaje = f"{error}"
        return JsonResponse({'mensaje': mensaje}, status=500)



def RegistrarPagoInicial(request, id):
    """
Esta función maneja el registro del pago inicial para un plan de pago y realiza las siguientes acciones:
- Registra la información del pago, incluyendo el valor de la cuota inicial, el valor pendiente, el valor del recaudo y la imagen de la factura de pago.
- Actualiza el estado del inmueble asociado a "Vendido".
- Devuelve una respuesta HTTP con un mensaje de éxito o un mensaje de error.

Args:
    request (HttpRequest): La solicitud HTTP recibida.
    id (int): El ID del plan de pago al que se va a registrar el pago inicial.

Returns:
    HttpResponse: Una respuesta HTTP que indica si el registro del pago inicial fue exitoso o si se produjo un error.
"""
    if request.method == 'POST':
        try:
            valorPago = request.POST.get('txtCuotaInicial')
            valorPendiente = request.POST.get('txtValorPendiente')
            recaudo = request.POST.get('txtCuotaInicial')  # Corregido: 'Recaudo' en lugar de 'CuotaInicial'
            foto = request.FILES.get("fileFoto")
            regpago = PlanDePago.objects.get(pk=id)
            cuota = 1
            
            with transaction.atomic():
                # Registra la información del pago inicial
                pago = RegistroPago(
                    regValorPago=valorPago,
                    regPendiente=valorPendiente,
                    regRecaudo=recaudo,  
                    regPlanDePago=regpago,
                    regFoto=foto,
                    regNumCuota=cuota
                )
                
                pago.save()
                
                venta = Venta.objects.get(pk=id)
                inmuebl = venta.venInmueble.id
                inmueble = Inmueble.objects.get(pk=inmuebl)
                
                # Actualiza el estado del inmueble a "Vendido"
                inmueble.inmEstado = "Vendido"
                inmueble.save()
                
                mensaje = "Pago Registrado correctamente"
                retorno = {"mensaje": mensaje, "estado": True}
                
                return render(request, "asesor/vistaListarVentasSeparadas.html", retorno)
        except Exception as error:
            mensaje = f"{error}"
            retorno = {"mensaje": mensaje, "estado": False}
            return render(request, "asesor/vistaListarVentasSeparadas.html", retorno)


def obtenerPagosRegistrados(request, id):
    """
Esta función obtiene información sobre los pagos registrados para un plan de pago específico y devuelve los datos en formato JSON.

Args:
    request (HttpRequest): La solicitud HTTP recibida.
    id (int): El ID de la venta asociada al plan de pago.

Returns:
    HttpResponse: Una respuesta HTTP en formato JSON que contiene la información de los pagos registrados.
    En caso de error, se devuelve un mensaje de error con un código de estado HTTP 500.
"""
    # Obtiene el plan de pago asociado a la venta
    planpag = PlanDePago.objects.filter(plaVenta=id).first()
    idPlan = planpag.id
    
    # Obtiene el primer registro de pago asociado al plan de pago
    registroPagos = RegistroPago.objects.filter(regPlanDePago=idPlan).first()
    
    try:
        # Crea un diccionario 'registroPago' con la información relevante de los pagos registrados
        registroPago = {
            'numCuotas': planpag.plaNumCuota,
            'id': registroPagos.id,
            'valorPago': planpag.plaValorDeCuota,
            'fechaInicio': planpag.plaFechaInicial,
            'fechaPago': registroPagos.regFechaPago,
            'numCuota': registroPagos.regNumCuota,
            'valorPendiente': registroPagos.regPendiente,
            'valorRecaudado': registroPagos.regRecaudo,
        }
        
        retorno = {'registroPago': registroPago}
        
        # Devuelve una respuesta JSON con la información de los pagos registrados.
        return JsonResponse(retorno)
    
    except Error as error:
        # En caso de error, devuelve un mensaje de error con un código de estado HTTP 500.
        mensaje = f"{error}"
        return JsonResponse({'mensaje': mensaje}, status=500)

    

def actualizarPago(request, id):
    """
Esta función maneja la actualización de un registro de pago y realiza las siguientes acciones:
- Actualiza la fecha de pago, el valor de la cuota, el valor pendiente, el valor total, y el número de cuota en el registro de pago.
- Actualiza la imagen de la factura de pago si se proporciona una nueva imagen.
- Marca la venta asociada como no morosa.
- Devuelve una respuesta HTTP con un mensaje de éxito o un mensaje de error.

Args:
    request (HttpRequest): La solicitud HTTP recibida.
    id (int): El ID del registro de pago que se va a actualizar.

Returns:
    HttpResponse: Una respuesta HTTP que indica si la actualización fue exitosa o si se produjo un error.
"""
    if request.method == 'POST':
        try:
            fechapago = request.POST.get('txtFechaPago')
            valorcuota = request.POST.get('txtValorCuota')
            pendiente = request.POST.get('txtValorPendiente')
            total = request.POST.get('txtValorPagoTotal')
            numcuota = request.POST.get('txtNumCuota')
            foto = request.FILES.get("fileFoto")
            
            with transaction.atomic():
                registro = RegistroPago.objects.filter(pk=id).first()
                registro.regFechaPago = fechapago
                registro.regValorPago = valorcuota
                registro.regPendiente = pendiente
                registro.regRecaudo = total
                registro.regNumCuota = numcuota
                
                # Actualiza la imagen de la factura de pago si se proporciona una nueva imagen
                if foto:
                    os.remove('./media/'+str(registro.regFoto))
                    registro.regFoto = foto
                    
                registro.save()
                
                planPago = PlanDePago.objects.get(pk=registro.regPlanDePago.id)
                venta = Venta.objects.get(pk=planPago.plaVenta.id)
                
                # Marca la venta asociada como no morosa
                venta.venEstadoMora = False
                venta.save()
                
                mensaje = "Pago Registrado correctamente"
                retorno = {"mensaje": mensaje, "estado": True}
                return render(request, 'asesor/vistaListarVentasVendidas.html', retorno)
        
        except Error as error:
            transaction.rollback()
            mensaje = f"{error}"
            retorno = {"mensaje": mensaje, "estado": False}
        
        return render(request, 'asesor/vistaListarVentasVendidas.html', retorno)

def verificarDesistimiento():
    """
Esta función se encarga de verificar si ha pasado un cierto
número de días desde la fecha de separación de inmuebles en estado 
"Separado" y tomar acciones en consecuencia, como cambiar el estado del inmueble o enviar 
correos electrónicos de notificación.

Returns:
    None
"""
    try:
        # Obtiene todas las separaciones en estado "Separado"
        inmuebles_separados = Inmueble.objects.filter(inmEstado="Separado")

        # Obtiene la fecha actual
        fecha_actual = datetime.now()

        # Itera a través de las separaciones y verifica si han pasado 3 días o 2 días
        for inmueble in inmuebles_separados:
            venta = Venta.objects.filter(venInmueble=inmueble.id).first()
            fecha_separacion = venta.venFechaSeparacion  # Asegúrate de tener un campo para la fecha de separación en tu modelo Inmueble

            # Convierte la fecha de separación a datetime
            fecha_separacion_datetime = datetime.combine(fecha_separacion, datetime.min.time())

            if fecha_actual - fecha_separacion_datetime >= timedelta(days=3):
                # Cambia el estado del inmueble a "Disponible" si han pasado 3 días
                inmueble.inmEstado = "Disponible"
                inmueble.save()
                asunto = 'Liberacion de Inmueble Sistema InmoSoft'
                mensajeCorreo = f'Cordial saludo, <b>{venta.venCliente.cliNombre} {venta.venCliente.cliApellido}</b>, nos permitimos.\
                informarle que el inmueble que usted ha separado de un proyecto, no se le ha realizado el primer pago acordado\
                por lo tanto este inmueble quedará disponible nuevamente para su venta a partir de este momento.<br>\
                <br><br>Para cualquier duda, lo invitamos a ingresar a nuestro sistema en la URL:\
                https://inmosoft.pythonanywhere.com'
                thread = threading.Thread(
                    target=enviarCorreo, args=(asunto, mensajeCorreo, [venta.venCliente.cliCorreo]))
                thread.start()
            elif fecha_actual - fecha_separacion_datetime >= timedelta(days=2):
                # Envía un correo electrónico de notificación si han pasado 2 días
                asunto = 'Liberacion de Inmueble Sistema InmoSoft'
                mensajeCorreo = f'Cordial saludo, <b>{venta.venCliente.cliNombre} {venta.venCliente.cliApellido}</b>, nos permitimos.\
                informarle que el inmueble que usted ha separado de un proyecto, no se le ha realizado el primer pago acordado\
                por lo tanto este inmueble quedará disponible nuevamente para su venta dentro de 1 día. Por favor, realice el pago.<br>\
                <br><br>Para cualquier duda, lo invitamos a ingresar a nuestro sistema en la URL:\
                https://inmosoft.pythonanywhere.com'
                thread = threading.Thread(
                    target=enviarCorreo, args=(asunto, mensajeCorreo, [venta.venCliente.cliCorreo]))
                thread.start()
    except Exception as e:
        # Maneja cualquier error que pueda ocurrir durante la verificación
        print(f"Error en la verificación de desistimiento: {e}")


def listarVentasSeparadas(request):
    """
Esta función se encarga de listar las ventas separadas por el usuario actual.

Args:
    request (HttpRequest): La solicitud HTTP recibida.

Returns:
    HttpResponse: Una respuesta HTTP en formato JSON que contiene la lista de ventas separadas y su información asociada.
    En caso de error, se devuelve un mensaje de error con un código de estado HTTP 500.
"""
    try:
        # Inicializa una lista vacía para almacenar la información de las ventas separadas.
        ventas = []
        
        # Filtra las ventas separadas para el usuario actual.
        ventasModel = Venta.objects.filter(venUsuario=request.user, venInmueble__inmEstado='Separado')
        
        # Itera sobre la lista de ventas separadas.
        for venta in ventasModel:
            # Crea un diccionario 'ven' con la información relevante de la venta separada.
            ven = {
                'idVen': venta.id,
                'id': venta.venInmueble.id,
                'cliente': f"{venta.venCliente.cliNombre} {venta.venCliente.cliApellido}",
                'proyecto': venta.venInmueble.inmProyecto.proNombre,
                'estado': venta.venInmueble.inmEstado,
            }
            
            # Agrega los datos de la venta separada a la lista 'ventas'.
            ventas.append(ven)
        
        # Devuelve una respuesta JSON con la lista de ventas separadas.
        return JsonResponse({'ventas': ventas})
    
    except Error as error:
        # En caso de error, devuelve un mensaje de error con un código de estado HTTP 500.
        mensaje = f"{error}"
        return JsonResponse({'mensaje': mensaje}, status=500)

    
def listarVentasVendidas(request):
    """
Esta función se encarga de listar las ventas vendidas por el usuario actual que no se encuentren en estado de mora.

Args:
    request (HttpRequest): La solicitud HTTP recibida.

Returns:
    HttpResponse: Una respuesta HTTP en formato JSON que contiene la lista de ventas vendidas y su información asociada.
    En caso de error, se devuelve un mensaje de error con un código de estado HTTP 500.
"""
    try:
        # Inicializa una lista vacía para almacenar la información de las ventas vendidas.
        ventas = []
        
        # Filtra las ventas vendidas para el usuario actual que no están en estado de mora.
        ventasModel = Venta.objects.filter(venUsuario=request.user, venInmueble__inmEstado='Vendido', venEstadoMora=False)
        
        # Itera sobre la lista de ventas vendidas.
        for venta in ventasModel:
            # Crea un diccionario 'ven' con la información relevante de la venta vendida.
            ven = {
                'idVen': venta.id,
                'id': venta.venInmueble.id,
                'cliente': f"{venta.venCliente.cliNombre} {venta.venCliente.cliApellido}",
                'proyecto': venta.venInmueble.inmProyecto.proNombre,
                'estado': venta.venInmueble.inmEstado,
            }
            
            # Agrega los datos de la venta vendida a la lista 'ventas'.
            ventas.append(ven)
        
        # Devuelve una respuesta JSON con la lista de ventas vendidas.
        return JsonResponse({'ventas': ventas})
    
    except Error as error:
        # En caso de error, devuelve un mensaje de error con un código de estado HTTP 500.
        mensaje = f"{error}"
        return JsonResponse({'mensaje': mensaje}, status=500)

    
def EnviarListaMora(request, id):
    """
Esta función maneja la lógica para enviar a un cliente a la lista de mora si no ha completado su pago de un inmueble.
Además, envía un correo electrónico de notificación al cliente.

Args:
    request (HttpRequest): La solicitud HTTP recibida.
    id (int): El ID de la venta asociada al cliente.

Returns:
    HttpResponse: Una respuesta HTTP que indica si el cliente ha sido enviado a la lista de mora y si se envió el correo electrónico.
"""
    try:
        # Obtiene la venta correspondiente al ID proporcionado.
        venta = Venta.objects.filter(pk=id).first()
        
        # Obtiene el plan de pago asociado a la venta.
        plapago = PlanDePago.objects.filter(plaVenta=venta.id).first()
        
        # Obtiene el registro de pago asociado al plan de pago.
        registroPago = RegistroPago.objects.filter(regPlanDePago=plapago.id).first()
        
        if registroPago.regNumCuota < plapago.plaNumCuota:
            # Si el número de cuota actual es menor que el total de cuotas, cambia el estado de mora a True.
            venta.venEstadoMora = True
            venta.save()
            estado = True
            mensaje = "El Cliente se ha enviado a la lista de mora"
            
            # Configura los datos para enviar un correo electrónico de notificación.
            asunto = 'Lista de mora Sistema InmoSoft'
            mensajeCorreo = f'Cordial saludo, <b>{venta.venCliente.cliNombre} {venta.venCliente.cliApellido}</b>, nos permitimos\
            informarle que el inmueble que usted ha separado de un proyecto, actualmente se encuentra atrasado en su último pago.\
            Por favor, realice el pago lo antes posible.<br>\
            <br><br>Para cualquier duda, lo invitamos a ingresar a nuestro sistema en la URL:\
            https://inmosoft.pythonanywhere.com'
            
            # Inicia un subproceso para enviar el correo electrónico de notificación.
            thread = threading.Thread(
                target=enviarCorreo, args=(asunto, mensajeCorreo,[venta.venCliente.cliCorreo]))
            thread.start()
        else:
            estado = False
            mensaje = "Este Cliente ha completado su pago"
        
        retorno = {"mensaje": mensaje, "estado": estado}
        
        # Renderiza una vista de lista de ventas vendidas con el resultado del proceso.
        return render(request, 'asesor/vistaListarVentasVendidas.html', retorno)
    
    except Error as error:
        # En caso de error, realiza un rollback de la transacción y muestra un mensaje de error.
        transaction.rollback()
        mensaje = f"{error}"
        retorno = {"mensaje": mensaje, "estado": False}
        
        # Renderiza una vista de lista de ventas vendidas con el mensaje de error.
        return render(request, 'asesor/vistaListarVentasVendidas.html', retorno)

    
def ObtenerListaMora(request):
    """
Esta función obtiene una lista de ventas en mora para el usuario actual y devuelve la información relevante en formato JSON.

Args:
    request (HttpRequest): La solicitud HTTP recibida.

Returns:
    HttpResponse: Una respuesta HTTP en formato JSON que contiene la lista de ventas en mora y su información asociada.
    En caso de error, se devuelve un mensaje de error con un código de estado HTTP 500.
"""
    try:
        # Inicializa una lista vacía para almacenar la información de ventas en mora.
        Mora = []
        
        # Filtra las ventas en mora para el usuario actual.
        listaMora = Venta.objects.filter(venUsuario=request.user, venEstadoMora=True)
        
        # Itera sobre la lista de ventas en mora.
        for usumora in listaMora:
            # Obtiene el plan de pago asociado a la venta en mora.
            planPago = PlanDePago.objects.filter(plaVenta=usumora.id).first()
            
            # Obtiene el registro de pago asociado al plan de pago.
            registroPago = RegistroPago.objects.filter(regPlanDePago=planPago.id).first()
            
            # Crea un diccionario 'mora' con la información relevante de la venta en mora.
            mora = {
                'idVen': usumora.id,
                'id': usumora.venInmueble.id,
                'cliente': f"{usumora.venCliente.cliNombre} {usumora.venCliente.cliApellido}",
                'proyecto': usumora.venInmueble.inmProyecto.proNombre,
                'estado': usumora.venInmueble.inmEstado,
                'numCuotaActual': registroPago.regNumCuota,
                'idRegistroPago': registroPago.id,
            }
            
            # Agrega los datos de la venta en mora a la lista 'Mora'.
            Mora.append(mora)
        
        # Devuelve una respuesta JSON con la lista de ventas en mora.
        return JsonResponse({'ListaMora': Mora})
    
    except Error as error:
        # En caso de error, devuelve un mensaje de error con un código de estado HTTP 500.
        mensaje = f"{error}"
        return JsonResponse({'mensaje': mensaje}, status=500)


def numeroVentasPorAsesor(request, filtro_tiempo=None):
    """
Esta función se encarga de calcular y proporcionar datos de ventas por asesor en función de un período de tiempo especificado.

Args:
    request (HttpRequest): La solicitud HTTP recibida.
    filtro_tiempo (str, opcional): Un parámetro que determina el período de tiempo para filtrar las ventas.
        Puede ser 'Mensual', 'Trimestral', 'Semestral', 'Anual' o None (sin filtro de tiempo).

Returns:
    HttpResponse: Una respuesta HTTP en formato JSON que contiene los datos de ventas por asesor si la operación se realiza con éxito.
    En caso de error, se devuelve una respuesta con un mensaje de error y un código de estado HTTP 500.
"""
    try:
        # Inicializa una lista vacía para almacenar los datos de ventas por asesor.
        numeroVentasPorAsesor = []
        
        # Obtiene una lista de ventas y cuenta las ventas por cada usuario.
        ventas = Venta.objects.values('venUsuario__username').annotate(numero_ventas=Count('id')).filter(venInmueble__inmEstado='Vendido')

        # Aplica un filtro de tiempo si se proporciona un valor para filtro_tiempo.
        if filtro_tiempo == 'Mensual':
            ventas = ventas.filter(venFechaSeparacion__gte=mes_pasado())
        elif filtro_tiempo == 'Trimestral':
            ventas = ventas.filter(venFechaSeparacion__gte=trimestre_pasado())
        elif filtro_tiempo == 'Semestral':
            ventas = ventas.filter(venFechaSeparacion__gte=semestre_pasado())
        elif filtro_tiempo == 'Anual':
            ventas = ventas.filter(venFechaSeparacion__gte=last_year())

        # Itera sobre la lista de ventas resultante.
        for venta in ventas:
            # Obtiene todas las ventas del asesor actual.
            ventas_del_asesor = Venta.objects.filter(venUsuario__username=venta['venUsuario__username'])
            
            # Encuentra la fecha de última modificación de las ventas del asesor.
            ultima_modificacion = ventas_del_asesor.latest('venFechaSeparacion').venFechaSeparacion
            
            # Obtiene información del usuario asociado al asesor.
            usuario = User.objects.filter(username=venta['venUsuario__username']).first()
            
            # Crea un diccionario con la información del asesor y sus ventas.
            venta_data = {
                'username': f"{usuario.first_name} {usuario.last_name}",
                'numeroVenta': venta['numero_ventas'],
                'ultimaModificacion': ultima_modificacion.strftime('%Y-%m-%d')
            }
            
            # Agrega los datos de ventas por asesor a la lista.
            numeroVentasPorAsesor.append(venta_data)

        # Devuelve una respuesta JSON con los datos de ventas por asesor.
        return JsonResponse({'numeroVentasPorAsesor': numeroVentasPorAsesor})
    
    except Exception as error:
        # En caso de error, devuelve un mensaje de error con un código de estado HTTP 500.
        mensaje = f"{error}"
        return JsonResponse({'mensaje': mensaje}, status=500)

# Funciones de ayuda para calcular fechas pasadas

# Esta función calcula la fecha que corresponde al mes pasado a partir de la fecha actual.
def mes_pasado():
    today = datetime.now()
    last_month = today - timedelta(days=30)
    return last_month

# Esta función calcula la fecha que corresponde al trimestre pasado a partir de la fecha actual.
def trimestre_pasado():
    today = datetime.now()
    last_quarter = today - timedelta(days=90)
    return last_quarter

# Esta función calcula la fecha que corresponde al semestre pasado a partir de la fecha actual.
def semestre_pasado():
    today = datetime.now()
    last_half_year = today - timedelta(days=180)
    return last_half_year

# Esta función calcula la fecha que corresponde al año pasado a partir de la fecha actual.
def last_year():
    today = datetime.now()
    last_year = today - timedelta(days=365)
    return last_year


from django.db.models.functions import ExtractMonth, ExtractYear
import calendar

def ventas_por_mes(request):
    meses_espanol = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

    ventas_por_mes = (
        Venta.objects
        .annotate(month=ExtractMonth('venFechaSeparacion'))
        .annotate(year=ExtractYear('venFechaSeparacion'))
        .values('month', 'year')
        .annotate(total=Count('id'))
        .order_by('year', 'month')
        .filter(venInmueble__inmEstado='Vendido')
    )

    data = {
        'labels': [f"{meses_espanol[mes['month'] - 1]} {mes['year']}" for mes in ventas_por_mes],
        'data': [mes['total'] for mes in ventas_por_mes],
    }

    return JsonResponse(data)
    
#-----------------------------/APIS/-----------------------------------------

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class ClienteInteresadoList(generics.ListCreateAPIView):
    serializer_class = ClienteInteresadoSerializer
    def get_queryset(self):
        proyecto = self.kwargs['proyecto'] 
        return ClienteInteresado.objects.filter(cliProyecto=proyecto)
