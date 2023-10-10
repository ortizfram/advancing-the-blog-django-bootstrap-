from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.accounts import views

urlpatterns = [
    # admin panel
    path('admin/', admin.site.urls),
    
    # authentication 
    #path("login/", login_view, name='login'),
    #path("logout/", logout_view, name='logout'),
    path("register/", views.register , name='register'),


    # apps
    path("comments/", include("apps.comments.urls")),
    path("posts/", include("apps.posts.urls"), name='posts'),
    path("store/", include("apps.store.urls"), name='store'),
    path("", include("apps.landing.urls"), name='home'),
]

# for online static
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

