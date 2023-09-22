from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json

def store(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, "store.html", context)

def updateItem(request):
    response_data = {'message': '# Item was added'}

    data = json.loads(request.body.decode('utf-8'))
    productId = data['productId']
    action = data['action']
    print("Action:", action)
    print("ProductId:", productId)

    if request.user.is_authenticated:
        customer = request.user.customer
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)

        # Save the orderItem
        orderItem.save()

        # Check if the quantity is less than or equal to 0 and delete the orderItem
        if orderItem.quantity <= 0:
            orderItem.delete()

        # Calculate the updated cart total
        cart_total = order.get_cart_items

        # Include the cart_total in the response
        response_data['cart_total'] = cart_total

    return JsonResponse(response_data)



def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,
                                                     complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
    context = {"items":items, "order":order}
    return render(request, "cart.html", context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,
                                                     complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
    context = {"items":items, "order":order}
    return render(request, "checkout.html", context)