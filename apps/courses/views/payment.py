from django.shortcuts import render,redirect
from apps.courses.models import Course
from django.contrib import messages
from urllib.parse import urlencode
from django.urls import reverse

def payment_success(request, slug):
    course = Course.objects.get(slug=slug)
    context = {
        'course' : course,
        # Add more context data as needed
    }
    return render(request, 'courses/payment/payment_success.html', context=context)

def payment_failed(request, slug):
    course = Course.objects.get(slug=slug)
    context = {
        'course' : course,
        # Add more context data as needed
    }
    return render(request, 'courses/payment/payment_failed.html', context=context)