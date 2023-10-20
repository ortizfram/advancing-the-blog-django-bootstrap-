from django.urls import path
from apps.courses.views import courses_view

app_name = 'courses'

urlpatterns = [
    path('', courses_view, name='courses_view'),
]
