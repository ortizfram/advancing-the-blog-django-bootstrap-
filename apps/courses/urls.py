from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from apps.courses.views import courses_view, course_detail, checkout, payment_failed, payment_success

app_name = 'courses'

urlpatterns = [
    path('', courses_view, name='courses_view'),
    path('<str:slug>/', course_detail, name='course_detail'),
    path('checkout/<str:slug>/', checkout, name='course_checkout'),
    path('checkout/<str:slug>/payment_success', payment_success, name='payment_success'),
    path('checkout/<str:slug>/payment_failed', payment_failed, name='payment_failed'),
    path('', include('paypal.standard.ipn.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)