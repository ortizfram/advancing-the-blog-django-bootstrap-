from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json

def store(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, "store.html", context)

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

            product = Product.objects.get(id=productId)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)

            # Define orderItem before accessing its properties
            orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

            if action == 'add':
                orderItem.quantity += 1
            elif action == 'remove':
                orderItem.quantity -= 1

                # Check if the quantity is less than or equal to 0 and delete the orderItem
                if orderItem.quantity <= 0:
                    orderItem.delete()

            # Save the orderItem
            orderItem.save()

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
    else:
        response_data['message'] = 'Invalid request method'

        # Set cart_total to 0 for non-POST and non-GET requests
        response_data['cart_total'] = 0

    return JsonResponse(response_data)


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
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
        except Customer.DoesNotExist:
                customer = None  # Handle the case where Customer doesn't exist for this user
        else:
            customer = None
        order, created = Order.objects.get_or_create(customer=customer,
                                                     complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
    context = {"items":items, "order":order}
    return render(request, "checkout.html", context)