from django.shortcuts import render,redirect
from apps.courses.models import Course, Video
from django.contrib import messages
from urllib.parse import urlencode
from django.urls import reverse

# Create your views here.
def courses_view(request):
    courses = Course.objects.all()
    return render (request, 'courses/courses.html', context={"courses":courses})

def course_detail(request, slug):
    course = Course.objects.get(slug=slug)
    serial_number = request.GET.get('lecture')#from searchbar after click on lecture
    if serial_number is None : # for lecture [0]
        serial_number = 1
    videos = course.video_set.all().order_by("serial_number")
    # ↓ return course and video lecture from video Model serial_number from Yt when uploading 
    # ↓ then ask it in frontend passing video_id to player and each video has it's {{video.serial_number}}">{{video}} 
    video = Video.objects.get(serial_number = serial_number, course = course)
    print(serial_number, video)
    print("Preview video", video.is_preview)
    # ↓ login to see if enrolled when clicking see more
    # ↓ after login go back to course to see videos
    if ((request.user.is_authenticated is False) and (video.is_preview is False)):
        messages.info(request, "You must be logged in to see more.")
        # Construct the URL for the login page with the 'next' parameter
        login_url = reverse('login')  # Replace 'login' with your login URL name
        next_param = urlencode({'next': request.get_full_path()})
        redirect_url = f'{login_url}?{next_param}'
        return redirect(redirect_url)

    # if enrolled you can see any video...

    context = {
        'course' : course,
        'video': video,
        'videos': videos,
    }
    return render(request, 'courses/course_detail.html', context=context)