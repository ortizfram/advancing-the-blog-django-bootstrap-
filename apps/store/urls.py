from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    
    path('cart/update_item/', views.updateItem, name='update_item'),# store JsonResponse +: for template
    path('update_item/', views.updateItem, name='update_item'),
]