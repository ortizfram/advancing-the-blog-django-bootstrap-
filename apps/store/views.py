from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import CheckoutForm

def store(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, "store.html", context)

# endpoint view: update_item
def updateItem(request):
    response_data = {'message': '', 'cart_total': 0}

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        productId = data.get('productId')
        action = data.get('action')

        if request.user.is_authenticated:
            try:
                customer = request.user.customer
            except Customer.DoesNotExist:
                customer = None
            order, created = Order.objects.get_or_create(customer=customer, complete=False)

            product = Product.objects.get(id=productId)

            # Define orderItem before accessing its properties
            orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

            if action == 'add':
                orderItem.quantity += 1
            elif action == 'remove':
                orderItem.quantity -= 1

            if orderItem.quantity <= 0:
                orderItem.delete()
            else:
                # Save the orderItem
                orderItem.save()

            # Check if the order is empty (no items left)
            if order.orderitem_set.count() == 0:
                order.complete = True
                order.save()

            # Calculate the updated cart total and quantity
            cart_items = order.orderitem_set.all()
            cart_total = sum(item.product.price * item.quantity for item in cart_items)
            cart_quantity = sum(item.quantity for item in cart_items)

            # Calculate the updated total price for the specific item
            item_total_price = product.price * orderItem.quantity

            # Include the cart_total, cart_quantity, and item_total_price in the response
            response_data['cart_total'] = cart_total
            response_data['cart_quantity'] = cart_quantity
            response_data['item_total_price'] = item_total_price
            response_data['quantity'] = orderItem.quantity

        else:
            customer = None
            response_data['message'] = 'User is not authenticated'

    elif request.method == 'GET':
        # Handle GET request to calculate and return the cart total
        if request.user.is_authenticated:
            try:
                customer = request.user.customer
            except Customer.DoesNotExist:
                customer = None

            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            cart_items = order.orderitem_set.all()
            cart_total = sum(item.product.price * item.quantity for item in cart_items)
            cart_quantity = sum(item.quantity for item in cart_items)

            response_data['cart_total'] = cart_total
            response_data['cart_quantity'] = cart_quantity
        else:
            response_data['message'] = 'User is not authenticated'
            order = None
            items = []
    else:
        response_data['message'] = 'Invalid request method'

        # Set cart_total to 0 for non-POST and non-GET requests
        response_data['cart_total'] = 0

    return JsonResponse(response_data)

# endpoint view: process_order
@csrf_exempt
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


def cart(request):
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
        except Customer.DoesNotExist:
            customer = None

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    
    context = {"items": items, "order": order}
    return render(request, "cart.html", context)

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
    context = {"items": items, "order": order, "shipping_required": shipping_required, "checkout_form": checkout_form,}
    return render(request, "checkout.html", context)


