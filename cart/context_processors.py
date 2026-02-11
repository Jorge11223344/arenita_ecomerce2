def cart_info(request):
    cart = request.session.get('cart', {})
    total_items = sum(item.get('quantity', 0) for item in cart.values())
    total_price = 0
    for item in cart.values():
        try:
            price = float(item.get('price', 0))
            qty = int(item.get('quantity', 0))
            total_price += price * qty
        except Exception:
            pass
    return {'cart_items_count': total_items, 'cart_total_price': total_price}
