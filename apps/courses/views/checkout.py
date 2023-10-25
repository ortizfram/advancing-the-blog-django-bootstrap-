from django.shortcuts import render,redirect
from apps.courses.models import Course
from django.contrib import messages
from urllib.parse import urlencode
from django.urls import reverse
from paypal.standard.forms import PaypalPaymentsForm
from django.conf import settings
import uuid

def checkout(request, slug):
    course = Course.objects.get(slug=slug)
    # Calculate the amount with the discount applied
    amount = course.price - (course.price * (course.discount / 100))

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
    # ☻↓ if enrolled you can see the video...

    # ☻↓ request domain: x.com
    host = request.get_host()

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': amount, # Assign the calculated amount with the discount
        'item_name': course.name,
        'invoice': uuid.uuid4(), #generate random id
        'currency_code': 'USD',
        'notify_url':  f"https://{host}{reverse('paypal-ipn')}",# send payment req to this endpoin inside library django-paypal
        'return_url': f"",
    }

    context = {
        'course' : course,
        # Add more context data as needed
    }
    return render(request, 'courses/checkout/checkout.html', context=context)

