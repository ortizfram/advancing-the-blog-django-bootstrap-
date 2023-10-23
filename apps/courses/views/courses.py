from django.shortcuts import render
from apps.courses.models import Course

# Create your views here.
def courses_view(request):
    courses = Course.objects.all()
    return render (request, 'courses/courses.html', context={"courses":courses})

def course_detail(request, slug):
    course = Course.objects.get(slug=slug)
    context = {
        'course' : course
    }
    return render(request, 'courses/course_detail.html', context=context)