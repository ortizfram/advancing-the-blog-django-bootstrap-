from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.accounts.views import (
    login_view,
    register_view,
    logout_view,
)

urlpatterns = [
    # user registration
    path("login/", login_view, name='login'),
    path("logout/", logout_view, name='logout'),
    path("register/", register_view, name='register'),

    # apps
    path('admin/', admin.site.urls),
    path("comments/", include("apps.comments.urls")),
    path("posts/", include("apps.posts.urls")),
]

# for online static
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

