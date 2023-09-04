from django.contrib import admin

# Register your models here.
from apps.posts.models import Post

class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title","updated","timestamp"]
    list_display_link = ["updated"]
    list_filter = ["updated","timestamp"]
    search_fileds= ["title","content"]
    class Meta:
        model = Post

admin.site.register(Post, PostModelAdmin)