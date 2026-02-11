from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from decimal import Decimal
from django.core.mail import send_mail
from django.conf import settings

from cart.cart import Cart
from .forms import CheckoutForm
from .models import Order, OrderItem


def checkout(request):
    """
    Vista de checkout para procesar el formulario de compra.
    """
    cart = Cart(request)
    if len(cart) == 0:
        messages.info(request, "Tu carro está vacío.")
        return redirect('cart_detail')
    
    print("=== CHECKOUT DEBUG ===")
    print("HOST:", request.get_host())
    print("ORIGIN:", request.headers.get("Origin"))
    print("REFERER:", request.headers.get("Referer"))




    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # 1) Crear la Orden
            total = cart.get_total_price()
            order = Order.objects.create(
                nombre=form.cleaned_data['nombre'],
                apellido=form.cleaned_data['apellido'],
                direccion=form.cleaned_data['direccion'],
                email=form.cleaned_data['email'],
                telefono=form.cleaned_data['telefono'],
                total=Decimal(total),
                estado='pendiente'
            )
            
            # 2) Crear los OrderItem desde el carro
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    nombre=item['product'].nombre,
                    precio=item['price'],
                    cantidad=item['quantity']
                )

            # 3) NO limpiamos el carro aquí - esperamos confirmación de pago
            # El carro se limpiará en payments/views.py después del pago exitoso
            # Esto previene que el usuario pierda su carrito si el pago falla

            # 4) Redirigir a página "Listo para pagar"
            messages.info(request, f"Orden #{order.id} creada. Procede al pago.")
            return redirect('orders_pay', order_id=order.id)
    else:
        form = CheckoutForm()

    # Render con el resumen del carro
    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart': cart,
        'total': cart.get_total_price(),
    })


def pay(request, order_id):
    """
    Pantalla "Listo para pagar".
    Muestra resumen de la orden antes de iniciar el pago con Transbank.
    """
    order = get_object_or_404(Order, pk=order_id)
    
    # Verificar que la orden está pendiente
    if order.estado not in ['pendiente', 'fallida']:
        messages.warning(request, f"Esta orden ya está {order.estado}.")
        return redirect('inicio')
    
    return render(request, 'orders/pay.html', {'order': order})
