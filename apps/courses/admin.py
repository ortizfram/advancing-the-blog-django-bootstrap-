from django.contrib import admin
# ↓ after importing it in __init__
from .models import Course, Learning, Prerequisite, Tag

# Register your models here.

admin.site.register(Course)
admin.site.register(Learning)
admin.site.register(Prerequisite)
admin.site.register(Tag)