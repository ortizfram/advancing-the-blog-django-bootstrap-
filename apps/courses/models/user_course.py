from django.db import models
from django.conf import settings
from .course import Course

class UserCourse(models.Model):
    course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, null=False, on_delete=models.CASCADE) #superadmin default
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.course.name}'