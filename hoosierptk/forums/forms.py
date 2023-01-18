from django import forms
from .models import Post

# New Post Form
class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ("title", "content", "topic", "tags")
