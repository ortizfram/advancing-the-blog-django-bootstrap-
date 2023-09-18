from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Comment
from .forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from .models import Comment

def comment_thread(request, id):
    parent_comment = get_object_or_404(Comment, id=id)
    children_comments = Comment.objects.filter(parent=parent_comment)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        print(request.POST)  # Debug: Print POST data to check form submission data

        if comment_form.is_valid():
            parent_id = request.POST.get("parent_id")
            object_id = request.POST.get("object_id")
            content_type_str = request.POST.get("content_type")  # Get the content_type string

            try:
                # Try to get the ContentType instance for the content_type string
                content_type = ContentType.objects.get(model=content_type_str)
            except ContentType.DoesNotExist:
                # Handle the case where the ContentType doesn't exist
                content_type = None

            print(f"parent_id: {parent_id}")  # Debug: Print parent_id to check

            if parent_id:
                # Handle child comment submission
                parent_comment = get_object_or_404(Comment, id=parent_id)
                new_comment = comment_form.save(commit=False)
                new_comment.user = request.user
                new_comment.parent = parent_comment
                new_comment.object_id = object_id
                
                # Set the content_type instance, and check if it exists
                if content_type:
                    new_comment.content_type = content_type
                else:
                    # Handle the case where content_type is not found (you can customize this part)
                    # You might want to raise an error, log a message, or handle it differently
                    # For now, we'll set a default content_type for demonstration purposes
                    new_comment.content_type = ContentType.objects.get_for_model(Comment)  # Replace YourModel with your actual model
                    
                new_comment.save()
            else:
                # Handle parent comment submission
                new_comment = comment_form.save(commit=False)
                new_comment.user = request.user
                new_comment.object_id = object_id
                
                # Set the content_type instance, and check if it exists
                if content_type:
                    new_comment.content_type = content_type
                else:
                    # Handle the case where content_type is not found (you can customize this part)
                    # You might want to raise an error, log a message, or handle it differently
                    # For now, we'll set a default content_type for demonstration purposes
                    new_comment.content_type = ContentType.objects.get_for_model(Comment)  # Replace YourModel with your actual model
                    
                new_comment.save()
    
    else:
        # When rendering the form, populate content_type, object_id, and parent_id from the parent comment
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