from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from shop.models import Category, Product
from .cart import Cart


class CartTest(TestCase):
    """Tests para el carrito de compras"""
    
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            nombre="Test Category",
            slug="test-category"
        )
        self.product = Product.objects.create(
            categoria=self.category,
            nombre="Test Product",
            slug="test-product",
            precio=Decimal('10000'),
            activo=True
        )
    
    def test_add_to_cart(self):
        """Test de agregar producto al carrito"""
        response = self.client.post(
            reverse('cart_add', args=[self.product.id]),
            {'quantity': 2}
        )
        self.assertEqual(response.status_code, 302)  # Redirect
        
        # Verificar que el producto está en la sesión
        session = self.client.session
        cart_data = session.get('cart', {})
        self.assertIn(str(self.product.id), cart_data)
    
    def test_cart_detail_view(self):
        """Test de vista de detalle del carrito"""
        # Agregar producto al carrito
        self.client.post(
            reverse('cart_add', args=[self.product.id]),
            {'quantity': 1}
        )
        
        # Ver carrito
        response = self.client.get(reverse('cart_detail'))
        self.assertEqual(response.status_code, 200)
    
    def test_remove_from_cart(self):
        """Test de eliminar producto del carrito"""
        # Agregar producto
        self.client.post(
            reverse('cart_add', args=[self.product.id]),
            {'quantity': 1}
        )
        
        # Eliminar producto
        response = self.client.post(
            reverse('cart_remove', args=[self.product.id])
        )
        self.assertEqual(response.status_code, 302)
        
        # Verificar que el carrito está vacío
        session = self.client.session
        cart_data = session.get('cart', {})
        self.assertEqual(len(cart_data), 0)
    
    def test_cart_total_price(self):
        """Test del cálculo del total del carrito"""
        # Agregar 2 productos
        self.client.post(
            reverse('cart_add', args=[self.product.id]),
            {'quantity': 2}
        )
        
        response = self.client.get(reverse('cart_detail'))
        # El total debería ser 20000 (10000 * 2)
        self.assertContains(response, '20000')
