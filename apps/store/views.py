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


@csrf_exempt
def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, "store.html", context)

# endpoint view: update_item
@csrf_exempt
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
@csrf_exempt
@login_required
def processOrder(request):
    print('Data:', request.body)
    transaction_id = datetime.datetime.now().timestamp()

    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError as e:
        # Handle invalid JSON data
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    customer = None

    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=request.user, name=request.user.username, email=request.user.email)
        print(f"Created customer profile for {request.user.username}")

    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    # Check if 'form' key exists in the data dictionary
    if 'form' in data:
        form_data = data['form']
        total = form_data.get('total', '0.00')
        total = float(total)  # Convert total to float here

        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

    if 'shipping' in data and isinstance(data['shipping'], dict):
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping'].get('address', ''),
            country=data['shipping'].get('country', ''),
            state=data['shipping'].get('state', ''),
            zipcode=data['shipping'].get('zipcode', ''),
        )

    return JsonResponse({'message': 'Payment completed'})

@csrf_exempt
def cart(request):
    session_id = request.session.session_key  # Get the session ID
    if session_id is None:
        request.session.save()  # Generate a new session key
    if request.user.is_authenticated:
        # Authenticated user
        try:
            customer = request.user.customer
        except Customer.DoesNotExist:
            customer = None
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
    else:
        # Non-authenticated user
        items = []
        order, created = Order.objects.get_or_create(session_id=session_id, complete=False)

    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'cart.html', context)
    
    # ... rest of your view ...

@csrf_exempt
def checkout(request):
    # Instantiate the form
    checkout_form = CheckoutForm()

    if request.user.is_authenticated:
        try:
            customer = request.user.customer
        except Customer.DoesNotExist:
            customer = None
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        # Debugging: Print the values of item.product.digital for each item
        for item in items:
            print(f"Product {item.product.name}, Digital: {item.product.digital}")
        # Check if any product in the order needs shipping
        shipping_required = any(item.product.digital is False for item in items)
        print("Shipping Required:", shipping_required)
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        shipping_required = False  # Set to False for anonymous users
    context = {"items": items, "order": order, "shipping_required": shipping_required, "checkout_form": checkout_form}
    return render(request, "checkout.html", context)
