from .models import Cart

def send_cart_length(request):
    cart_length = 0
    total = 0

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_length = cart.get_total_items()
            total = cart.get_total_price()
        except Cart.DoesNotExist:
            cart_length = 0
            total = 0
    else:
        cart_length = 0

    return {'cart_length': cart_length, 'total': total}
