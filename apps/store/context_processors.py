from .models import Order, Customer

def cart_count(request):
    cart_total = 0
    
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
        except Customer.DoesNotExist:
                customer = None  # Handle the case where Customer doesn't exist for this user
        else:
            customer = None
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cart_total = order.get_cart_items

    return {'cart_count': cart_total}
