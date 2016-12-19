"""This module is for python forms."""
from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """This is form for our Post model."""

    class Meta:
        model = Post
        fields = ('title', 'text')


class CommentForm(forms.ModelForm):
    """Comment model form."""

    class Meta:
        model = Comment
        fields = ('author', 'text')
