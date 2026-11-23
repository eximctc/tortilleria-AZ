from django.test import TestCase
from django.test import override_settings
from django.contrib.auth import get_user_model

from .models import Categoria, Cliente, Producto


@override_settings(ALLOWED_HOSTS=["testserver"])
class TiendaViewsTests(TestCase):
    def test_inicio_muestra_categorias_y_productos_activos(self):
        categoria = Categoria.objects.create(nombre="Tortillas")
        Producto.objects.create(
            nombre="Tortilla de maíz",
            precio="20.00",
            stock=10,
            categoria=categoria,
        )
        Producto.objects.create(
            nombre="Producto inactivo",
            precio="15.00",
            stock=0,
            categoria=categoria,
            activo=False,
        )

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tortillas")
        self.assertContains(response, "Tortilla de maíz")
        self.assertNotContains(response, "Producto inactivo")

    def test_hola_mundo(self):
        response = self.client.get("/hola/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "¡Hola Mundo desde mi proyecto de negocio!")

    def test_dashboard_redirige_a_login_si_no_hay_sesion(self):
        response = self.client.get("/dashboard/")

        self.assertRedirects(response, "/login/?next=/dashboard/")

    def test_dashboard_muestra_resumen_a_usuario_autenticado(self):
        usuario = get_user_model().objects.create_user(username="admin", password="pass123")
        self.client.force_login(usuario)
        categoria = Categoria.objects.create(nombre="Tortillas")
        Producto.objects.create(
            nombre="Tortilla de maíz",
            precio="20.00",
            stock=10,
            categoria=categoria,
        )
        Producto.objects.create(
            nombre="Producto sin stock",
            precio="15.00",
            stock=0,
            categoria=categoria,
            activo=False,
        )
        Cliente.objects.create(
            nombre="Cliente de prueba",
            email="cliente@example.com",
            telefono="5551234567",
            direccion="Dirección de prueba",
        )

        response = self.client.get("/dashboard/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tortillas")
        self.assertContains(response, "Productos por categoría")
        self.assertContains(response, "Producto sin stock")
        self.assertEqual(response.context["total_productos"], 2)
        self.assertEqual(response.context["total_clientes"], 1)
        self.assertEqual(response.context["productos_activos"], 1)
        self.assertEqual(response.context["productos_sin_stock"], 1)
        self.assertEqual(response.context["valor_inventario"], 35)
        self.assertEqual(response.context["por_categoria"][0].num_productos, 2)

    def test_cerrar_sesion_por_post_redirige_a_inicio(self):
        usuario = get_user_model().objects.create_user(username="admin", password="pass123")
        self.client.force_login(usuario)

        response = self.client.post("/logout/")

        self.assertRedirects(response, "/")
        self.assertNotIn("_auth_user_id", self.client.session)
