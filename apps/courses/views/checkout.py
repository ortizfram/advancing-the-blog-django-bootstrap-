from django.shortcuts import render,redirect
from apps.courses.models import Course
from django.contrib import messages
from urllib.parse import urlencode
from django.urls import reverse

def checkout(request, slug):
    course = Course.objects.get(slug=slug)

    # Process the enrollment and payment with PayPal integration here
    # ...


    # ↓ login before enrolling
    if not request.user.is_authenticated:
        messages.info(request, "You must be logged in to see more.")
        # Construct the URL for the login page with the 'next' parameter
        login_url = reverse('login')  # Replace 'login' with your login URL name
        next_param = urlencode({'next': request.get_full_path()})
        redirect_url = f'{login_url}?{next_param}'
        return redirect(redirect_url)
    # ↓ if enrolled you can see any video...
    context = {
        'course' : course,
        # Add more context data as needed
    }
    return render(request, 'courses/checkout.html', context=context)