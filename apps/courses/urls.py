from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from apps.courses.views import courses_view, course_detail

app_name = 'courses'

urlpatterns = [
    path('', courses_view, name='courses_view'),
    path('<str:slug>/', course_detail, name='course_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)