from django.urls import path
from . import views

app_name = 'about'

urlpatterns = [
    # pages
    path('', views.about, name='about'),
   
]