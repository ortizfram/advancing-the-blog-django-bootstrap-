from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, ProfileUsernameForm
from .models import Profile
from django.contrib.auth import login
from .forms import EmailUpdateForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            login(request, user)
            messages.success(
                request, f"Hi {username}, your account was created successfully"
            )

            return redirect("/")
    else:
        form = UserRegisterForm()

    return render(request, "accounts/register.html", {"form": form})


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
    """Request user and user Profile, if does not exist, create one
    based on Profile model that takes user. Combines UserRegisterForm and
    ProfileUpdateForm, if the form has changed save, alert, redirect."""
    user = request.user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=user)

    if request.method == "POST":
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user)

        if profile_form.is_valid():
            profile_form_has_changed = profile_form.has_changed()
            login(request, user)

            if profile_form_has_changed:
                profile_form.save()

                messages.success(request, "Your profile has been updated.")
            else:
                messages.info(request, "No changes were made to your profile.")

            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")

    else:
        profile_form = ProfileUpdateForm(instance=profile)

    return render(
        request, "accounts/profile_update.html", {"profile_form": profile_form}
    )


@login_required
def profile_update_username(request):
    user = request.user
    if request.method == "POST":
        user_form = ProfileUsernameForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            login(request, user)
            messages.success(request, "Your username has been updated.")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = ProfileUsernameForm(instance=request.user)

    return render(
        request, "accounts/profile_update_username.html", {"user_form": user_form}
    )


@login_required
def email_update(request):
    user = request.user
    if request.method == "POST":
        email_form = EmailUpdateForm(request.POST)

        if email_form.is_valid():
            new_email = email_form.cleaned_data["new_email"].lower()
            request.user.email = new_email
            request.user.save()
            login(request, user)
            messages.success(request, "Your email address has been updated.")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        email_form = EmailUpdateForm()

    return render(request, "accounts/email_update.html", {"email_form": email_form})