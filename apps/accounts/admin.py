from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """This is made to display in admin pannel the model CustomUser,
    inheriting UserAdmin class from base User auth. It only need to be maid the main one throuh settings.AUTH_USER_MODEL
    """
    list_display = ('username', 'email', 'first_name', 'surname', 'phone', 'profile_image', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'surname')
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'surname', 'phone', 'profile_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    
    def get_search_results(self, request, queryset, search_term):
        # This method retrieves the search results
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(id=search_term_as_int)
        except ValueError:
            pass
        return queryset, use_distinct

admin.site.register(CustomUser, CustomUserAdmin)