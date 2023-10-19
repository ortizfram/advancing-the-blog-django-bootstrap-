from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.accounts import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    # admin panels
    path('admin/', admin.site.urls),
    
    # authentication 
    path("register/", views.register , name='register'),
    path("profile/", views.profile , name='profile'),
    path("profile/manage_staff_users/", include("apps.accounts.urls"), name="manage_staff_users"),
    path("profile/update", views.profile_update , name='profile_update'),
    path('profile/update/username/', views.profile_update_username, name='profile_update_username'),
    path('email_update/', views.email_update, name='email_update'),
    path("login/", views.CustomLoginView.as_view(template_name='accounts/login.html'), name='login'),
    path("logout/", auth_view.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    
    # reset password
    path('reset_password/',auth_view.PasswordResetView.as_view(template_name='accounts/password_reset/reset_password.html'),name='reset_password'),
    path('reset_password_sent/',auth_view.PasswordResetDoneView.as_view(template_name='accounts/password_reset/reset_password_sent.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='accounts/password_reset/reset_password_confirm.html'),name='password_reset_confirm'),
    path('reset_password_complete/',auth_view.PasswordResetCompleteView.as_view(template_name='accounts/password_reset/reset_password_complete.html'),name='password_reset_complete'),

    # apps
    path("comments/", include("apps.comments.urls")),
    path("posts/", include("apps.posts.urls"), name='posts'),
    path("store/", include("apps.store.urls"), name='store'),
    path("", include("apps.landing.urls")),
]

# for online static
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

