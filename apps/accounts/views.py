from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, ProfileUsernameForm
from .models import Profile
from django.contrib.auth import login
from .forms import EmailUpdateForm
from django.db.models import Q
from apps.store.models import Customer
from django.contrib.auth import views as auth_views


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")

            # Check if the user has a customer profile
            if hasattr(user, 'customer'):
                customer = user.customer
                print("requested customer:",customer)
            else:
                # If not, create a Customer object for the user
                customer = Customer(user=user, name=username, email=email)
                customer.save()
                print("new customer:",customer)

            login(request, user)
            messages.success(
                request, f"Hi {username}, your account was created successfully"
            )

            return redirect("/")
    else:
        form = UserRegisterForm()

    return render(request, "accounts/register.html", {"form": form})


class CustomLoginView(auth_views.LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)

        if self.request.user.is_authenticated:
            # Check if the user has a customer profile
            if hasattr(self.request.user, 'customer'):
                customer = self.request.user.customer
                print("Requested customer:", customer)
            else:
                # If not, create a Customer object for the user
                customer = Customer(user=self.request.user, name=self.request.user.username, email=self.request.user.email)
                customer.save()
                print("New customer:", customer)

        # You don't need to manually return the response
        return super().form_valid(form)
    
# def logout(request):  // no need to, same as above
# here we use just a template login and a url: in urls.py
# from django.contrib.auth import views as auth_view




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


from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model


def is_staff_or_admin(view_func):
    """Custom decorator: for manage_staff_users view"""

    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden(
                "Access denied. You must be a staff member or administrator to access this page."
            )

    return _wrapped_view


@login_required
@is_staff_or_admin
def manage_staff_users(request):
    User = get_user_model()
    search_query = request.GET.get("q")

    if search_query:
        search_results = User.objects.filter(
            Q(username__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(first_name__icontains=search_query)
            | Q(surname__icontains=search_query)
        )
    else:
        # If no search query, fetch all users
        search_results = User.objects.all()

    if not search_results:
        message = "No search results found."

    return render(
        request,
        "accounts/admin_and_staff/manage_staff_users.html",
        {"users": search_results, "message": message if not search_results else ""},
    )
