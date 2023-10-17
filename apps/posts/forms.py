from django import forms
from pagedown.widgets import PagedownWidget
from .models import Post
from django.utils import timezone

class PostForm(forms.ModelForm):
    # Use PagedownWidget for the 'content' field
    content = forms.CharField(widget=PagedownWidget(attrs={'id': 'real-time-content'}))
    
    # Set the default value for 'publish' to the current date and time
    publish = forms.DateTimeField(initial=timezone.now)
    
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'image',
            'draft',
            'publish',
        ]
        
        widgets = {
            # Apply the PagedownWidget with the specified ID for 'content'
            'content': PagedownWidget(attrs={'id': 'real-time-content'}),
        }
