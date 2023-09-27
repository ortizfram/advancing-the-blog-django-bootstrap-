from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # pages
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    
    # endpoints : update_item
    path('cart/update_item/', views.updateItem, name='update_item'),# store JsonResponse +: for template
    path('checkout/update_item/', views.updateItem, name='update_item'),
    path('update_item/', views.updateItem, name='update_item'),

    # endpoints : process_order
    path('process_order/', views.processOrder, name='process_order'),
    path('checkout/process_order/', views.processOrder, name='process_order'),
    path('checkout/update_item/process_order/', views.processOrder, name='process_order'),
]