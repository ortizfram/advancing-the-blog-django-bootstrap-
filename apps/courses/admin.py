from django.contrib import admin
# ↓ after importing it in __init__ you can call as if it was in models.py
from .models import Course, Learning, Prerequisite, Tag

# Register your models here.

# ☻ Create inline admin classes for related models...
# ↓  These will be displayed within the CourseAdmin page.
class TagAdmin(admin.TabularInline):
    model = Tag

class LearningAdmin(admin.TabularInline):
    model = Learning

class PrerequisiteAdmin(admin.TabularInline):
    model = Prerequisite

# ☻ Create the CourseAdmin class that will be used to customize
# ↓  the admin interface for the Course model.
class CourseAdmin(admin.ModelAdmin):
    # Include the inline admin classes for related models.
    inlines = [TagAdmin, LearningAdmin, PrerequisiteAdmin]

# ☻↓ Register the Course model with the custom admin interface.
admin.site.register(Course, CourseAdmin)
