from django.contrib import admin
from .models import Course # after importing it in __init__

# Register your models here.

admin.site.register(Course)