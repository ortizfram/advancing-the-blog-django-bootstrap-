# apps/comments/views.py

from django.shortcuts import render, get_object_or_404
from .models import Comment
from .forms import CommentForm

def comment_thread(request, id):
    parent_comment = get_object_or_404(Comment, id=id)
    children_comments = Comment.objects.filter(parent=parent_comment)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        print(request.POST)  # Debug: Print POST data to check form submission data

        if comment_form.is_valid():
            parent_id = request.POST.get("parent_id")
            print(f"parent_id: {parent_id}")  # Debug: Print parent_id to check

            if parent_id:
                # Handle child comment submission
                parent_comment = get_object_or_404(Comment, id=parent_id)
                new_comment = comment_form.save(commit=False)
                new_comment.user = request.user
                new_comment.parent = parent_comment
                new_comment.save()
            else:
                # Handle parent comment submission
                new_comment = comment_form.save(commit=False)
                new_comment.user = request.user
                new_comment.save()
    
    else:
        comment_form = CommentForm()

    context = {
        "parent_comment": parent_comment,
        "children_comments": children_comments,
        "comment_form": comment_form,
    }

    return render(request, "comment_thread.html", context)
