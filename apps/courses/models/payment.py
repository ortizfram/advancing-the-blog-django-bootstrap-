from django.db import models
from django.conf import settings
from .course import Course
from .user_course import UserCourse

class Payment(models.Model):
    order_id = models.CharField(max_length=50, null=False)
    payment_id = models.CharField(max_length=50)
    user_course= models.ForeignKey(UserCourse, null=True, blank=True, on_delete=models.CASCADE, related_name='payments_for_user_courses')
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE)
    date= models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'order_id: {self.order_id}'