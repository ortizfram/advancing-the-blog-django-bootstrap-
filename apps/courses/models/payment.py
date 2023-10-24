from django.db import models
from django.conf import settings
from .course import Course

class Payment(models.Model):
    order_id = models.CharField(max_length=50, null=False)
    payment_id = models.CharField(max_length=50)
    user_course= models.ForeignKey(Course, null=False, on_delete=models.CASCADE)
    date= models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    # def __str__(self):
    #     return f'{self.user.username} - {self.course.name}'