from django.shortcuts import render, get_object_or_404
from .models import Comment  # Import your Comment model

def comment_thread(request, id):
    obj = get_object_or_404(Comment, id=id)
    comments = Comment.objects.filter(parent=obj)  # Get child comments for the current comment
    
    # You may want to pass a comment form to your template if needed
    # comment_form = YourCommentForm()  # Replace with your actual comment form
    
    context = {
        "comment": obj,
        "comments": comments,  # Pass child comments to the template
        # "comment_form": comment_form,  # Include the comment form if needed
    }
    return render(request, "comment_thread.html", context)
