"""This module is for python forms."""
from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """This is form for our Post model."""

    class Meta:
        model = Post
        fields = ('title', 'text')
