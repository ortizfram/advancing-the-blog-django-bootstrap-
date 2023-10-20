from django.shortcuts import render
from apps.courses.models import Course

# Create your views here.
def courses_view(request):
    courses = Course.objects.all()
    print(courses)
    return render (request, 'courses/courses.html', context={"courses":courses})