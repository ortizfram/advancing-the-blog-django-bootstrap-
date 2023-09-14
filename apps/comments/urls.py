from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/', views.comment_thread, name='thread'),
]
