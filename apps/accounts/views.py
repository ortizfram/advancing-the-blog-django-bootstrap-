from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile

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

@login_required
def profile_update(request):
    user = request.user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=user)

    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            # Check if the user_form or profile_form data has changed
            if user_form.has_changed() or profile_form.has_changed():
                # Save the form data only if it has changed
                if user_form.has_changed():
                    user_form.save()
                if profile_form.has_changed():
                    profile_form.save()

                messages.success(request, 'Your profile has been updated.')
            else:
                messages.info(request, 'No changes were made to your profile.')

            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        user_form = UserRegisterForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'accounts/profile_update.html', {'user_form': user_form, 'profile_form': profile_form})
