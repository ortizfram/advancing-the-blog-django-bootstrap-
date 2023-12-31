from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser

class UserRegisterForm(UserCreationForm):
    """Only for user registration"""
    email = forms.EmailField()

    class Meta:
        model = CustomUser  
        fields = ['username','email','password1','password2']

class ProfileUpdateForm(forms.ModelForm):
    """Update fileds once user is already registered, except username"""
    class Meta:
        model = CustomUser
        fields = ['profile_image', 'first_name', 'surname', 'phone']

class ProfileUsernameForm(UserCreationForm):
    """Update just username, to prevent saving error of username already in use"""
    class Meta:
        model = CustomUser  
        fields = ['username','password1','password2']

class EmailUpdateForm(forms.Form):
    new_email = forms.EmailField()