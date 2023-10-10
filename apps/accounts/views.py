from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth import login as auth_login
from django.db import IntegrityError
from .models import UserBase 


def login_view(request):
    next = request.GET.get('next')
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        user_name = form.cleaned_data.get("user_name")
        password = form.cleaned_data.get("password")
        user = authenticate(request, user_name=user_name, password=password)  # Use 'user_name' field for login
        if user:
            auth_login(request, user)
            if next:
                return redirect(next)
            return redirect("/")
    
    return render(request, "form.html", {"form": form, "title": title})


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_name = form.cleaned_data['user_name']
            email = form.cleaned_data['email']
            
            # Check if the user_name is already taken
            if UserBase.objects.filter(user_name=user_name).exists():
                form.add_error('user_name', 'This username is already taken.')
                return render(request, 'form.html', {'form': form, 'title': 'Register'})
            
            # Check if the email address is already registered
            if UserBase.objects.filter(email=email).exists():
                form.add_error('email', 'This email has already been registered.')
                return render(request, 'form.html', {'form': form, 'title': 'Register'})
            
            user.username = user_name
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            try:
                # Automatically log in the user after registration
                auth_login(request, user)
                return redirect("/")  # Redirect to the desired page after registration
            except IntegrityError as e:
                form.add_error('email', 'An error occurred while registering. Please try again.')
    else:
        form = UserRegisterForm()
    
    context = {'form': form, 'title': 'Register'}
    return render(request, 'form.html', context)

def logout_view(request):
    logout(request)
    return redirect('/')  # Redirect to the desired page after logout
