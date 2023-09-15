from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.urls import reverse
from urllib.parse import quote_plus
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .forms import CommentForm  

def comment_thread(request, id):
    obj = get_object_or_404(Comment, id=id)
    comments = Comment.objects.filter(parent=obj)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            # Create a new comment instance but don't save it yet
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user  # Set the comment's user to the logged-in user
            new_comment.content_type = ContentType.objects.get_for_model(obj)
            new_comment.object_id = obj.id

            # Set the parent comment if it's provided in the form data
            parent_id = request.POST.get("parent_id")
            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)
                new_comment.parent = parent_comment
            else:
                new_comment.parent = None  # This is a top-level comment

            # Save the comment
            new_comment.save()

            # Redirect to the same comment thread page after successful comment submission
            return HttpResponseRedirect(reverse('comments:thread', args=[id]))

    else:
        # Create a new empty form if the request method is GET
        comment_form = CommentForm()

    context = {
        "comment": obj,
        "comments": comments,
        "comment_form": comment_form,
    }
    
    return render(request, "comment_thread.html", context)
