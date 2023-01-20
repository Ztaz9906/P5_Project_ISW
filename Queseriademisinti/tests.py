from django.test import TestCase,Client
import Queseriademisinti.models as _
from .views import *
from django.db.utils import IntegrityError
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

class UserTestCase(TestCase):
    #Creando los usuarios para empezar las pruebas
    def setUp(self):
        self.superuser = get_user_model().objects.create_superuser(email='enrique@uci.cu', username="Enrique Ferreiro Avila",  dir="Uci", ci="99061417001", tfno="+5356562172", password='12345678',is_staff=True,is_cliente=True)
        self.user = get_user_model().objects.create_user(email='cliente@uci.cu', username="Cliente",  dir="Uci", ci="99110517011", tfno="+5356562171", password='12345678')
        pass
    def test_User_create(self):
        # Los Usuarios son creados correctamente
        superuser = User.objects.get(email="enrique@uci.cu")
        user = User.objects.get(email="cliente@uci.cu")
        self.assertEqual(superuser.username, 'Enrique Ferreiro Avila')
        self.assertEqual(user.tfno, '+5356562171')
        
    def test_User_edit(self):
        # Los Usuarios son editados correctamente correctamente
        user = User.objects.get(email="cliente@uci.cu")
        user.email = 'clienteedit@uci.cu'
        user.save()
        self.assertEqual(user.email, 'clienteedit@uci.cu')
        
    def test_User_delete(self):
        # Los Usuarios son borrados correctamente
        self.client.login(username='enrique@uci.cu', password='12345678')
        response = self.client.delete(reverse('eliminar_trabajador',kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/trabajador/'))
        
    def test_login(self):
        #el ususrio se logea correctamente
        self.client.login(username='enrique@uci.cu', password='12345678')
        response = self.client.get('/menu/')
        self.assertEqual(response.status_code, 200)
        
    def test_create_User_with_empty_fields(self):
        with self.assertRaises(IntegrityError):
             User.objects.create_user(email=None, username="Enrique Ferreiro Avila",  dir="Uci", ci="99061417001", tfno=None, password=None,is_staff=True,is_cliente=True)

    def test_delete_User_non_existing(self):
        with self.assertRaises(_.User.DoesNotExist):
            User.objects.get(pk="90")
            
class QuejasTestCase(TestCase):
    def setUp(self):
        self.superuser = get_user_model().objects.create_superuser(email='enrique@uci.cu', username="Enrique Ferreiro Avila",  dir="Uci", ci="99061417001", tfno="+5356562172", password='12345678',is_staff=True,is_cliente=True)
        self.user = User.objects.create_user(email='cliente@uci.cu', username="Cliente",  dir="Uci", ci="99110517011", tfno="+5356562171", password='12345678')
        pass
    def test_quejas_add(self):
        self.client.login(username='cliente@uci.cu', password='12345678')
        response = self.client.post(reverse('add_queja'), {'usuario_id':self.user.pk,'tipo': 'Q', 'descripcion':'Test', 'titulo': 'Queja'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/Quejas_y_sugerencias/'))
        Created = _.Quejas.objects.get(titulo="Queja")
        self.assertIsInstance(Created,_.Quejas)
        self.assertEqual(Created.titulo, 'Queja')
    def test_tus_quejas(self):
        self.client.login(username='cliente@uci.cu', password='12345678')
        response=self.client.get(reverse('quejas'))
        self.assertAlmostEqual(response.status_code, 200)
        
    def test_create_Quejas_with_empty_fields(self):
        with self.assertRaises(IntegrityError):
            _.Quejas.objects.create(usuario_id=None,tipo=None,descripcion=None,titulo=None)

    def test_delete_Quejas_non_existing(self):
        with self.assertRaises(_.Quejas.DoesNotExist):
            _.Quejas.objects.get(pk="90")
            
class RespuestaTestCase(TestCase):
    def setUp(self):
        self.superuser = get_user_model().objects.create_superuser(email='enrique@uci.cu', username="Enrique Ferreiro Avila",  dir="Uci", ci="99061417001", tfno="+5356562172", password='12345678',is_staff=True,is_cliente=True)
        self.user = User.objects.create_user(email='cliente@uci.cu', username="Cliente",  dir="Uci", ci="99110517011", tfno="+5356562171", password='12345678')
        self.quejas = _.Quejas.objects.create(usuario_id=self.user,tipo='Q',descripcion='Test',titulo='Queja')
        pass
        self.respuesta = _.Respuestas.objects.create(usuario_id=self.quejas.usuario_id,quejas_id=self.quejas,descripcion="Test")
    def test_add_respuesta(self):
        self.client.login(username='enrique@uci.cu', password='12345678')
        queja = _.Quejas.objects.get(usuario_id=self.user.pk)
        self.assertCountEqual(queja.titulo,'Queja')
        response = self.client.post(reverse('add_repuesta',kwargs={'pk': queja.pk}), {'usuario_id':queja.usuario_id.pk,'quejas_id': queja.pk, 'descripcion':'respuesta'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/respuestas/'))
         
    def test_edit_respuesta(self):
        respuesta = _.Respuestas.objects.get(quejas_id=self.quejas)
        respuesta.descripcion = 'Pablito'
        respuesta.save()
        self.assertEqual(respuesta.descripcion,'Pablito')
    
    def test_delete_respuesta(self):
        self.client.login(username='enrique@uci.cu', password='12345678')
        response = self.client.delete(reverse('eliminar_respuesta',kwargs={'pk': self.respuesta.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/respuestas/'))
        
    def test_client_respuestas(self):
        self.client.login(username='cliente@uci.cu', password='12345678')
        response = self.client.get(reverse('respuesta'))
        self.assertEqual(response.status_code, 200)
        
    def test_create_Respuestas_with_empty_fields(self):
        with self.assertRaises(IntegrityError):
            _.Respuestas.objects.create(usuario_id=None,quejas_id=None,descripcion=None)

    def test_delete_Respuestas_non_existing(self):
        with self.assertRaises(_.Respuestas.DoesNotExist):
            _.Respuestas.objects.get(pk="90")
            
class ProductTestCase(TestCase):
    def setUp(self):
        self.superuser = get_user_model().objects.create_superuser(email='enrique@uci.cu', username="Enrique Ferreiro Avila",  dir="Uci", ci="99061417001", tfno="+5356562172", password='12345678',is_staff=True,is_cliente=True)
        self.user = User.objects.create_user(email='cliente@uci.cu', username="Cliente",  dir="Uci", ci="99110517011", tfno="+5356562171", password='12345678')    
    def test_producto_create(self):
        self.client.login(username='enrique@uci.cu', password='12345678')
        response = self.client.get('/producto/')
        self.assertEqual(response.status_code, 200)
        myfile = SimpleUploadedFile(name='test_image.jpg', content=open(r'C:\Users\Z-TAZ\Music\Django-Posgres\Cafeteria\Queseriademisinti\static\images\carrusel-1.jpg', 'rb').read(), content_type='image/jpeg')
        response = self.client.post(reverse('add_producto'), {'foto':myfile,'nombre':'producto','precio': 100,'cantidad':100})
        self.assertEqual(response.status_code, 302)
        producto = _.Producto.objects.get(nombre="producto")
        self.assertIsInstance(producto,_.Producto)
    
    def test_edit_producto(self):
        self.client.login(username='enrique@uci.cu', password='12345678')
        myfile = SimpleUploadedFile(name='test_image.jpg', content=open(r'C:\Users\Z-TAZ\Music\Django-Posgres\Cafeteria\Queseriademisinti\static\images\carrusel-1.jpg', 'rb').read(), content_type='image/jpeg')
        response = self.client.post(reverse('add_producto'), {'foto':myfile,'nombre':'producto','precio': 100,'cantidad':100})
        self.assertEqual(response.status_code, 302)
        producto = _.Producto.objects.get(nombre="producto")
        producto.nombre='editado'
        producto.save()
        self.assertEqual(producto.nombre, 'editado')

    def test_delete_producto_non_existing(self):
        with self.assertRaises(_.Producto.DoesNotExist):
            _.Producto.objects.get(pk="90")
            
class PedidoTestCase(TestCase):
    def setUp(self):
        self.superuser = get_user_model().objects.create_superuser(email='enrique@uci.cu', username="Enrique Ferreiro Avila",  dir="Uci", ci="99061417001", tfno="+5356562172", password='12345678',is_staff=True,is_cliente=True)
        self.client.login(username='enrique@uci.cu', password='12345678')
        myfile = SimpleUploadedFile(name='test_image.jpg', content=open(r'C:\Users\Z-TAZ\Music\Django-Posgres\Cafeteria\Queseriademisinti\static\images\carrusel-1.jpg', 'rb').read(), content_type='image/jpeg')
        self.client.post(reverse('add_producto'), {'foto':myfile,'nombre':'producto','precio': 100,'cantidad':100}) 
        self.producto = _.Producto.objects.get(nombre="producto")
        self.pedido = _.Pedido()
        self.pedido.cantidad= 2
        self.pedido.estado='E'
        self.pedido.user_id= self.superuser
        self.pedido.producto_id = self.producto
        self.pedido.save()
        
    def test_add_pedido(self):
        self.client.login(username='enrique@uci.cu', password='12345678')
        producto = _.Producto.objects.get(nombre="producto")
        response = self.client.post(reverse('add_pedido', kwargs = {'pk': producto.id}), {'cantidad': 1,'user_id':self.superuser})
        self.assertEqual(response.status_code,302)
        
    def test_edit_pedido(self):
        self.assertIsInstance(self.pedido,_.Pedido)
        self.pedido.estado= 'En'
        self.assertEqual(self.pedido.estado,'En')
        
    def test_compra(self):
        compra = _.Compra_venta()
        compra.user_id = self.superuser
        compra.pedido_id = self.pedido
        compra.total_pagado = 200
        compra.save()
        self.assertAlmostEqual(compra.pedido_id, self.pedido)
        
    def test_delete_pedido(self):
        self.client.login(username='enrique@uci.cu', password='12345678')
        response = self.client.delete(reverse('eliminar_pedido',kwargs={'pk': self.pedido.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.__eq__('/pedidos/'))
    
    def test_crear_pedido_form(self):
        self.client.login(username='enrique@uci.cu', password='12345678')
        response = self.client.post(reverse('edit_pedido', kwargs = {'pk': self.pedido.id}), {'estado': 'A'})
        self.assertEqual(response.status_code,302)
        self.assertTrue(response.url.__eq__("/pedidos/"))
        self.assertEqual(_.Pedido.objects.get(
            estado='A').estado, 'A')
        
    def test_create_pedido_with_empty_fields(self):
        with self.assertRaises(IntegrityError):
            _.Pedido.objects.create(user_id=None,producto_id=None,estado=None,cantidad=None)

    def test_delete_pedido_non_existing(self):
        with self.assertRaises(_.Pedido.DoesNotExist):
            _.Pedido.objects.get(pk="90")