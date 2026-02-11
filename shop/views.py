from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from cart.forms import AddToCartForm

def tienda(request, categoria_slug=None):
    categoria = None
    categorias = Category.objects.all()
    productos = Product.objects.filter(activo=True)
    if categoria_slug:
        categoria = get_object_or_404(Category, slug=categoria_slug)
        productos = productos.filter(categoria=categoria)
    return render(request, 'shop/tienda.html', {'categoria': categoria, 'categorias': categorias, 'productos': productos})

def producto_detalle(request, slug):
    producto = get_object_or_404(Product, slug=slug, activo=True)
    form = AddToCartForm()
    return render(request, 'shop/producto_detalle.html', {'producto': producto, 'form': form})
