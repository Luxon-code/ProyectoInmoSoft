from django.test import TestCase,Client
from django.urls import reverse
from appInmoSoft.models import *

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

