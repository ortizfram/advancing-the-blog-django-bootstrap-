from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.list_items, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    # path('<slug>/delete/', views.post_delete, name='post_delete'),
]
