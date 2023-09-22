from .models import Order

def cart_count(request):
    cart_total = 0
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cart_total = order.get_cart_items()

    return {'cart_count': cart_total}
