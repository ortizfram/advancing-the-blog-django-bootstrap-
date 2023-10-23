from django.urls import path
from apps.courses.views import courses_view, course_detail

app_name = 'courses'

urlpatterns = [
    path('', courses_view, name='courses_view'),
    path('<str:slug>/', course_detail, name='course_detail'),
]
