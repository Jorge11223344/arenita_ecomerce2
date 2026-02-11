from django.db import models

# Create your models here.
from django.db import models

class Order(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente de pago'),
        ('pagada', 'Pagada'),
        ('fallida', 'Fallida'),
        ('cancelada', 'Cancelada'),
            # Operacionales (punto 3)
        ('pendiente_confirmacion', 'Pendiente confirmación (transferencia)'),
        ('contra_entrega', 'Contra entrega'),
        ('en_preparacion', 'En preparación'),
        ('en_despacho', 'En despacho'),
        ('entregada', 'Entregada'),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=30, choices=ESTADOS, default='pendiente')

    nombre = models.CharField(max_length=120)
    apellido = models.CharField(max_length=120)
    direccion = models.CharField(max_length=255)
    email = models.EmailField()
    telefono = models.CharField(max_length=30)

    total = models.DecimalField(max_digits=12, decimal_places=0, default=0)

    # Para guardar el token/ID de la transacción Transbank más adelante
    # 🔑 Webpay: identificador (buy_order) y token (token_ws)
    buy_order = models.CharField(max_length=50, blank=True, null=True)
    tbk_token = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return f"Orden #{self.id} - {self.nombre} {self.apellido} - {self.estado}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('shop.Product', on_delete=models.PROTECT)
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    cantidad = models.PositiveIntegerField()

    def subtotal(self):
        return self.precio * self.cantidad

    def __str__(self):
        return f"{self.nombre} x {self.cantidad}"
