from django.shortcuts import render
from .models import Comment  # Import your Comment model

def comment_thread(request, id):
    # Retrieve comments based on the comment ID (adjust this based on your Comment model)
    comments = Comment.objects.filter(parent_id=id)

    # Pass comments to the template
    return render(request, "comment_thread.html", {"comments": comments})