from django.shortcuts import render,redirect
from apps.courses.models import Course, Video
from django.contrib import messages

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
    if ((request.user.is_authenticated is False) and (video.is_preview is False)):
        messages.info(request, "You must be logged in to see more.")
        return redirect('login')
    context = {
        'course' : course,
        'video': video,
        'videos': videos,
    }
    return render(request, 'courses/course_detail.html', context=context)