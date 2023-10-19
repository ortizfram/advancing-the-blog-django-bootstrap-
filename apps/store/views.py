from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.http import HttpResponse
import json
import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import CheckoutForm
from django.core.exceptions import ObjectDoesNotExist
from .utils import cookieCart,cartData, guestOrder


def store(request):

    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products,'cartItems':cartItems}
    return render(request, "store/store.html", context)


# endpoint view: update_item
def updateItem(request):
    # Get the product_id and action from the request parameters
    product_id = request.GET.get('productId')
    action = request.GET.get('action')

    try:
        # Attempt to retrieve the product by ID
        product = Product.objects.get(id=product_id)
    except ObjectDoesNotExist:
        # Product not found, return an error response
        return JsonResponse({'error': f'Product not found for ID: {product_id}'}, status=404)

    # Session management logic
    session_id = request.session.session_key
    if session_id is None:
        request.session.save()
        session_id = request.session.session_key

    # Retrieve or create an order for the session
    order, created = Order.objects.get_or_create(session_id=session_id, complete=False)

    # Retrieve or create an order item for the product
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    # Update the quantity based on the action
    if action == 'add':
        order_item.quantity += 1
    elif action == 'remove':
        order_item.quantity -= 1

    # Save the order item
    order_item.save()

    # If the quantity reaches 0, delete the order item
    if order_item.quantity <= 0:
        order_item.delete()

    # Return a success response
    return JsonResponse({'message': 'Item was updated'})

# endpoint view: process_order
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
    else: 
        customer, order = guestOrder(request, data) # utils.py
            

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True :
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            country=data['shipping']['country'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    return JsonResponse({'message': 'Payment completed'})

def cart(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'order': order, 'items': items, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)
    

def checkout(request):

    checkout_form = CheckoutForm()
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    context = {"items": items, "order": order, "cartItems":cartItems, "checkout_form": checkout_form}
    return render(request, "store/checkout.html", context)
