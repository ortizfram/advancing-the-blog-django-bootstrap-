from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.manage_staff_users, name='manage_staff_users'),
]
