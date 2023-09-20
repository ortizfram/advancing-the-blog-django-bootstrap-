from django.shortcuts import render

# Create your views here.
def list_items(request):
    context = {}
    return render(request, "store.html", context)

def cart(request):
    context = {}
    return render(request, "cart.html", context)

def checkout(request):
    context = {}
    return render(request, "checkout.html", context)