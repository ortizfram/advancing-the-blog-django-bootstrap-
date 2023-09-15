from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Comment
from .forms import CommentForm

def comment_thread(request, id):
    parent_comment = get_object_or_404(Comment, id=id)
    children_comments = Comment.objects.filter(parent=parent_comment)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.parent = parent_comment
            new_comment.save()
            return HttpResponseRedirect(request.path_info)

    else:
        initial_data = {
            "content_type": parent_comment.content_type,
            "object_id": parent_comment.object_id,
            "parent_id": parent_comment.id,
        }
        comment_form = CommentForm(initial=initial_data)

    context = {
        "parent_comment": parent_comment,
        "children_comments": children_comments,
        "comment_form": comment_form,
    }

    return render(request, "comment_thread.html", context)
