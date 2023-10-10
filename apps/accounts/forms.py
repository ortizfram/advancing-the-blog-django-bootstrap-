from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm 
from .models import UserBase

User = get_user_model()

class UserRegisterForm(forms.ModelForm):
    user_name = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
    )
    email2 = forms.EmailField(
        label="Confirm Email",
        widget=forms.EmailInput(attrs={'placeholder': 'Confirm Email'}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
    )

    class Meta:
        model = UserBase
        fields = [
            "user_name",
            "email",
            "email2",
            "password"
        ]

    def clean_user_name(self):
        user_name = self.cleaned_data['user_name']
        if User.objects.filter(user_name=user_name).exists():
            raise ValidationError('This username is already taken.')
        return user_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email has already been registered.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        email2 = cleaned_data.get("email2")
        if email and email2 and email != email2:
            raise forms.ValidationError("Emails must match")

class UserLoginForm(AuthenticationForm):
    def clean(self):
        cleaned_data = super().clean()
        user_name = cleaned_data.get("user_name")  # Use 'email' field for email
        password = cleaned_data.get("password")
        if user_name and password:
            user = authenticate(self.request, user_name=user_name, password=password)  # Authenticate with 'username' as email
            if not user:
                raise forms.ValidationError("Invalid email or password.")
            if not user.is_active:
                raise forms.ValidationError("This user is no longer active.")
        return cleaned_data

