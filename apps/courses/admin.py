from django.contrib import admin
# ↓ after importing it in __init__ you can call as if it was in models.py
from .models import Course, Payment, UserCourse, Learning, Prerequisite, Tag, Video

# Register your models here.

# ☻ Create inline admin classes for related models...
# ↓  These will be displayed within the CourseAdmin page.
class TagAdmin(admin.TabularInline):#shows admin in row style
    model = Tag

class VideoAdmin(admin.TabularInline):# • StackedInline:shows admin in col style
    model = Video

class LearningAdmin(admin.TabularInline):
    model = Learning

class PrerequisiteAdmin(admin.TabularInline):
    model = Prerequisite

# ☻ Create the CourseAdmin class that will be used to customize
# ↓  the admin interface for the Course model.
class CourseAdmin(admin.ModelAdmin):
    # Include the inline admin classes for related models.
    inlines = [TagAdmin ,LearningAdmin, PrerequisiteAdmin, VideoAdmin]

# ☻↓ Register the Course model with the custom admin interface.
admin.site.register(Course, CourseAdmin)
admin.site.register(Video)
admin.site.register(Payment)
admin.site.register(UserCourse)
