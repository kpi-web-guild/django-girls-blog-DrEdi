"""All views are here."""
from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.


def post_list(request):
    """Show all your Post objects."""
    posts = Post.objects.all()
    return render(request, 'main/index.html', {'posts': posts})


def post_detail(request, pk):
    """Show info about one post user choosed."""
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'main/post_detail.html', {'post': post})
