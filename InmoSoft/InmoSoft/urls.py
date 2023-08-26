"""
URL configuration for InmoSoft project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from appInmoSoft import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.vistaPaginaPrincipal),
    path('vistaRegistrarUsuario/',views.vistaRegistrarUsuario),
    path("vistaModificarUsuario/",views.vistaModificarUsuario),
    path("vistaInicioSesion/",views.vistaIniciarSesion),
    path("vistaPerfilUsuario/",views.vistaPerfilUsuario),
    path('vistaRegistrarProyecto/',views.vistaRegistrarProyecto),
    path('vistaRegistarCasaoApartamento/',views.vistaRegistrarCasaoApartamento),
    path('vistaDetalleInmueble/<int:proyecto_id>/', views.vistaDetalleInmueble),
    path('vistaModificarProyecto/',views.vistaModificarProyecto),
    path("inicioAdministrador/",views.vistaInicioAdministrador),
    path('inicioAsesor/',views.vistaInicioAsesor),
    path('registrarUsuario/',views.registrarUsuario),
    path('getUsuarios/',views.getUsuarios),
    path('listarProyectos/',views.listarProyectos),
    path('proyectosCarrusel/',views.proyectosCarrusel),
    path('proyectoDetalleCarrusel/<int:id>',views.proyectoDetalleCarrusel),
    path('cambiarEstadoUsuario/<int:id>',views.cambiarEstadoUsuario),
    path('modificarUsuario/<int:id>',views.modificarDatosUserPerfil),
    path('cambiarContraseña/<int:id>',views.cambiarContraseñaUsuario),
    path('guardarDatosFormulario1/',views.datosFormulario1),
    path('registrarProyecto/',views.registrarProyecto),
    path('buscarProyecto/<int:id>/',views.buscarProyecto),
    path('modificarProyecto/<int:id>/',views.modificarProyecto),
    path('iniciarSesion/',views.iniciarSesion),
    path('Api/inicioSesion/<str:usuario>/<str:contraseña>',views.iniciarSesionAPI),
    path('cerrarSesion/',views.cerrarSesion),
    path("reset_password/",auth_views.PasswordResetView.as_view(template_name="recuperarContraseña/PasswordResetView.html"),name="password_reset"),
    path("reset_password_send/",auth_views.PasswordResetDoneView.as_view(template_name="recuperarContraseña/PasswordResetDoneView.html"),name="password_reset_done"),
    path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name="recuperarContraseña/PasswordResetConfirmView.html"),name="password_reset_confirm"),
    path("reset_password_complete/",auth_views.PasswordResetCompleteView.as_view(template_name="recuperarContraseña/PasswordResetCompleteView.html"),name="password_reset_complete"),
]

if settings.DEBUG:
    urlpatterns += static (settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)