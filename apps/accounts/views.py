from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was created successfully')
            return redirect("/")
    else:
        form = UserRegisterForm()
        
    return render(request, "accounts/register.html", {'form':form})

# def login(request):  // no need to
  # here we use just a template login and a url: in urls.py
  # from django.contrib.auth import views as auth_view
  # path("login/", auth_view.LoginView.as_view(template_name='accounts/login.html'), name='login'),


# def logout(request):  // no need to, same as above

@login_required
def profile(request):
    return render(request, "accounts/profile.html")