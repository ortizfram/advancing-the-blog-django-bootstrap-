from django import forms
from pagedown.widgets import PagedownWidget
from .models import Post

class PostForm(forms.ModelForm):
    # Use PagedownWidget for the 'content' field
    content = forms.CharField(widget=PagedownWidget(attrs={'id': 'real-time-content'}))
    
    # Use SelectDateWidget for the 'publish' field
    publish = forms.DateField(widget=forms.SelectDateWidget())
    
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
            # Use SelectDateWidget for 'publish'
            'publish': forms.SelectDateWidget(),
        }
