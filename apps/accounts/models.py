from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    '''Model extends the Built In User model, used for updating created user
    fields, and adding new fields like phone, profile-img, firstname, surname'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    surname = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username