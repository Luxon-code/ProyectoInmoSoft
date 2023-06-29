from datetime import date, datetime
from django.shortcuts import render, redirect
from appInmoSoft.models import *
from django.contrib.auth.models import Group
from django.db import Error, transaction
import random
import string
from django.contrib.auth import authenticate
from django.contrib import auth
from django.conf import settings
import urllib
import json
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
import threading
from smtplib import SMTPException
from django.http import JsonResponse
from django.db.models import Sum, Avg, Count

# Create your views here.
def vistaRegistrarUsuario(request):
    roles = Group.objects.all()
    retorno = {'roles': roles}
    return render(request,'administrador/registrarUsuario.html',retorno)

def vistaModificarUsuario(request):
    return render(request,'administrador/modificarUsuario.html')

def vistaPaginaPrincipal(request):
    return render(request,'paginaPrincipal.html')
def vistaIniciarSesion(request):
    return render(request,'inicioSesion.html')
def registrarUsuario(request):
    try:
        cedula = request.POST["txtCedula"]
        nombres = request.POST["txtNombres"]
        apellidos = request.POST["txtApellido"]
        correo = request.POST["txtCorreo"]
        telefono = request.POST["txtTelefono"]
        foto = request.FILES.get("fileFoto", False)
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
            retorno = {"mensaje": mensaje,"estado":True}
            # enviar correo al usuario
            asunto = 'Registro Sistema InmoSoft'
            mensaje = f'Cordial saludo, <b>{user.first_name} {user.last_name}</b>, nos permitimos.\
                informarle que usted ha sido registrado en el Sistema de Inmosoft de la ciudad de Neiva.\
                Nos permitimos enviarle las credenciales de Ingreso a nuestro sistema.<br>\
                <br><b>Username: </b> {user.username}\
                <br><b>Password: </b> {passwordGenerado}\
                <br><br>Lo invitamos a ingresar a nuestro sistema en la url:\
                http://Inmosoft.com'
            thread = threading.Thread(
                target=enviarCorreo, args=(asunto, mensaje, user.email))
            thread.start()
            return render(request, 'administrador/registrarUsuario.html',retorno)
    except Error as error:
        transaction.rollback()
        mensaje = f"{error}"
    retorno = {"mensaje": mensaje,"estado":False}
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
        string.ascii_uppercase + string.digits + string.punctuation
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
        