from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """This is made to display in admin pannel the model CustomUser,
    inheriting UserAdmin class from base User auth. It only need to be maid the main one throuh settings.AUTH_USER_MODEL
    """
    list_display = ('username', 'email', 'first_name', 'surname', 'phone', 'profile_image', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'surname', 'phone', 'profile_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
