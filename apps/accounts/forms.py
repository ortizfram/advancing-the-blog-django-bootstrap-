from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ['email', 'user_name', 'password1', 'password2']

    def clean_username(self):
        user_name = self.cleaned_data['user_name']
        if User.objects.filter(user_name=user_name).exists():
            raise ValidationError('This username is already taken.')
        return user_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email has already been registered.')
        return email


class UserLoginForm(AuthenticationForm):
    def clean(self):
        cleaned_data = super().clean()
        user_name = cleaned_data.get("user_name")
        password = cleaned_data.get("password")

        if user_name and not self.user_cache:
            raise ValidationError("Invalid username or password. Please try again.")
        elif password and not self.user_cache.check_password(password):
            raise ValidationError("Invalid username or password. Please try again.")

        return cleaned_data