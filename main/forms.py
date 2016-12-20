"""This module contains classes that represent Forms.

It's easier to use built-in forms because you don't need to think about
connection with DB, SQL query etc. Just write FormModel and views for it
"""
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
