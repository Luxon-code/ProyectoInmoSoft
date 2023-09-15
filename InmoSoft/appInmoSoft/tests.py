from .views import *
from django.test import TestCase,Client,RequestFactory
from django.urls import reverse
from appInmoSoft.models import *
import unittest
import json
from django.core.files.uploadedfile import SimpleUploadedFile
class ViewsTestCase(TestCase):
    def setUp(self):
        # Creamos un usuario para realizar pruebas de autenticación
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()

    def test_vista_pagina_principal(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'paginaPrincipal.html')

    def test_vista_iniciar_sesion(self):
        response = self.client.get('/vistaInicioSesion/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inicioSesion.html')

    def test_vista_registrar_usuario_autenticado(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/vistaRegistrarUsuario/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'administrador/registrarUsuario.html')


    def test_vista_modificar_usuario_autenticado(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/vistaModificarUsuario/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'administrador/modificarUsuario.html')
        
class CambiarEstadoUsuarioTest(TestCase):
    def setUp(self):
        # Crear un usuario para las pruebas
        self.user = User.objects.create_user(username='usuario_prueba', password='contrasena_prueba')
        self.user_id = self.user.id

    def test_cambiar_estado_usuario(self):
        # Obtener la URL de la vista cambiarEstadoUsuario
        url = reverse('cambiarEstadoUsuario', args=[self.user_id])

        # Simular una solicitud POST para cambiar el estado del usuario
        response = self.client.post(url)

        # Verificar que la respuesta sea un JSON
        self.assertIsInstance(response, JsonResponse)

        # Analizar el contenido JSON de la respuesta
        data = response.json()

        # Verificar que el cambio de estado fue exitoso
        self.assertTrue(data['estado'])

        # Verificar que el mensaje sea "Estado del usuario modificado"
        self.assertEqual(data['mensaje'], "Estado del usuario modificado")

        # Actualizar el usuario desde la base de datos
        self.user.refresh_from_db()

        # Verificar que el estado del usuario se haya cambiado
        self.assertFalse(self.user.is_active)  # El usuario debería estar inactivo después del cambio

    def test_cambiar_estado_superusuario(self):
        # Crear un superusuario para las pruebas
        superuser = User.objects.create_superuser(username='superusuario',userCedula="10793567",
                                                  email='superusuario@gmail.com',password='contrasena')

        # Obtener la URL de la vista cambiarEstadoUsuario para el superusuario
        url = reverse('cambiarEstadoUsuario', args=[superuser.id])

        # Simular una solicitud POST para cambiar el estado del superusuario
        response = self.client.post(url)

        # Verificar que la respuesta sea un JSON
        self.assertIsInstance(response, JsonResponse)

        # Analizar el contenido JSON de la respuesta
        data = response.json()

        # Verificar que el cambio de estado no fue exitoso
        self.assertFalse(data['estado'])

        # Verificar que el mensaje sea "Este usuario no se le puede cambiar el estado..."
        self.assertEqual(data['mensaje'], "Este usuario no se le puede cambiar el estado, ya que es el superuser del sistema")

        # Actualizar el superusuario desde la base de datos
        superuser.refresh_from_db()

        # Verificar que el estado del superusuario no se haya cambiado
        self.assertTrue(superuser.is_active)  # El superusuario debería seguir activo

class PruebaRegistrarUsuario(unittest.TestCase):
    def setUp(self):
        # Crea una factoría de solicitudes
        self.factory = RequestFactory()
    def test_registrar_usuario_exito(self):
        # Crea una solicitud POST con datos válidos
        data = {
            "txtCedula": "123456",
            "txtNombres": "Juan",
            "txtApellido": "Pérez",
            "txtCorreo": "juan@example.com",
            "txtTelefono": "1234567890",
            "fileFoto": "",
            "cbRol": 1,  # Suponiendo que 1 es un ID de rol válido
        }
        request = self.factory.post("/registrar/", data)
     
        # Llama a la función de vista
        response = registrarUsuario(request)
     
        # Verifica si la respuesta es exitosa (código de estado 200)
        self.assertEqual(response.status_code, 200)
     
if __name__ == "__main__":
    unittest.main()
    
class ListarProyectosTest(TestCase):
    def setUp(self):
        # Crear una ubicación de ejemplo
        self.ubicacion = Ubicacion.objects.create(ubiDepartamento="Departamento", ubiCuidad="Ciudad")

        # Crear un proyecto de ejemplo con una foto (puedes ajustar esto según tus modelos)
        self.foto = SimpleUploadedFile("test_image.jpg", content=b"", content_type="image/jpg")
        self.proyecto = Proyecto.objects.create(
            proNombre="Proyecto de Prueba",
            proTipo="Tipo de Prueba",
            proUbicacion=self.ubicacion,
            proDescripcion="Descripción de prueba",
            proFoto=self.foto,
            proFiducia="Fiducia de prueba",
            proTotalInmuebles=5,
            proEstado=True,
            proNumeroManzanasTorres=34,
            proCostoSeparacion=300000,
            proNumeroInmuebles=78,
            proNumeroDePisos=34,
            proCantidadParqueadero=45,
        )
        #crear un apartamento asociado al inmuble
        self.apartamento = Apartamento.objects.create(apaNumeroHabitaciones=33,apaAreaConstruida="43",
                                                      apaCategoria="Tipo A",apaPrecioVivienda=456789)
        # Crear un inmueble de ejemplo asociado al proyecto
        self.inmueble = Inmueble.objects.create(inmProyecto=self.proyecto,inmApartamento=self.apartamento)

    def test_listar_proyectos(self):
        # Obtener la URL de la vista listarProyectos
        url = reverse('listarProyectos')

        # Realizar una solicitud GET a la vista
        response = self.client.get(url)

        # Verificar que la respuesta sea exitosa (código de estado 200)
        self.assertEqual(response.status_code, 200)

        # Analizar el contenido JSON de la respuesta
        data = json.loads(response.content.decode('utf-8'))

        # Verificar que el proyecto creado se encuentra en la lista de proyectos
        self.assertEqual(len(data['proyectos']), 1)

        # Verificar que los detalles del proyecto son correctos en la respuesta JSON
        proyecto_respuesta = data['proyectos'][0]
        self.assertEqual(proyecto_respuesta['id'], self.proyecto.id)
        self.assertEqual(proyecto_respuesta['nombre'], self.proyecto.proNombre)
        self.assertEqual(proyecto_respuesta['tipo'], self.proyecto.proTipo)
        self.assertEqual(proyecto_respuesta['ubicacion'], f"{self.ubicacion.ubiDepartamento},{self.ubicacion.ubiCuidad}")
        self.assertEqual(proyecto_respuesta['descripcion'], self.proyecto.proDescripcion)
        self.assertEqual(proyecto_respuesta['precio'], f"{self.inmueble.inmApartamento.apaPrecioVivienda:,}")
        self.assertEqual(proyecto_respuesta['fiducia'], self.proyecto.proFiducia)
        self.assertEqual(proyecto_respuesta['totalinmuebles'], self.proyecto.proTotalInmuebles)