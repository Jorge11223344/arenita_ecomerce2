from django.db import models
from django.urls import reverse

class Category(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)

    class Meta:
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('tienda_categoria', args=[self.slug])

class Product(models.Model):
    categoria = models.ForeignKey(Category, related_name='productos', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)

    # ✅ NUEVO (punto 4): SKU y peso
    sku = models.CharField(max_length=64, unique=True, blank=True, null=True)
    peso_kg = models.DecimalField(max_digits=6, decimal_places=2, default=0, help_text="Peso del producto en kg")

    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=0, help_text="Precio en CLP")
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('producto_detalle', args=[self.slug])
