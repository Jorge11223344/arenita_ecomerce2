from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from .models import Category, Product


class CategoryModelTest(TestCase):
    """Tests para el modelo Category"""
    
    def setUp(self):
        self.category = Category.objects.create(
            nombre="Arena Aglutinante",
            slug="arena-aglutinante"
        )
    
    def test_category_creation(self):
        """Test de creación de categoría"""
        self.assertEqual(self.category.nombre, "Arena Aglutinante")
        self.assertEqual(str(self.category), "Arena Aglutinante")
    
    def test_category_get_absolute_url(self):
        """Test de URL de categoría"""
        url = self.category.get_absolute_url()
        self.assertEqual(url, '/tienda/categoria/arena-aglutinante/')


class ProductModelTest(TestCase):
    """Tests para el modelo Product"""
    
    def setUp(self):
        self.category = Category.objects.create(
            nombre="Arena Premium",
            slug="arena-premium"
        )
        self.product = Product.objects.create(
            categoria=self.category,
            nombre="Arena Super Premium 10kg",
            slug="arena-super-premium-10kg",
            sku="ASP-10KG-001",
            descripcion="Arena de alta calidad",
            precio=Decimal('15000'),
            peso_kg=Decimal('10.00'),
            activo=True
        )
    
    def test_product_creation(self):
        """Test de creación de producto"""
        self.assertEqual(self.product.nombre, "Arena Super Premium 10kg")
        self.assertEqual(self.product.precio, Decimal('15000'))
        self.assertEqual(str(self.product), "Arena Super Premium 10kg")
    
    def test_product_get_absolute_url(self):
        """Test de URL de producto"""
        url = self.product.get_absolute_url()
        self.assertEqual(url, '/tienda/producto/arena-super-premium-10kg/')
    
    def test_product_active_filtering(self):
        """Test de filtrado de productos activos"""
        Product.objects.create(
            categoria=self.category,
            nombre="Producto Inactivo",
            slug="producto-inactivo",
            precio=Decimal('5000'),
            activo=False
        )
        active_products = Product.objects.filter(activo=True)
        self.assertEqual(active_products.count(), 1)


class ShopViewsTest(TestCase):
    """Tests para las vistas de shop"""
    
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
    
    def test_store_view(self):
        """Test de vista de tienda"""
        response = self.client.get(reverse('store'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
    
    def test_product_detail_view(self):
        """Test de vista de detalle de producto"""
        response = self.client.get(
            reverse('producto_detalle', args=[self.product.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
    
    def test_category_view(self):
        """Test de vista de categoría"""
        response = self.client.get(
            reverse('tienda_categoria', args=[self.category.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Category')
