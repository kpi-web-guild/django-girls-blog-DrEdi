"""All views are here."""
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required


def post_list(request):
    """Show all your Post objects."""
    posts = Post.objects.all()
    return render(request, 'main/index.html', {'posts': posts})


def post_detail(request, pk):
    """Show info about one post you have chosen."""
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'main/post_detail.html', {'post': post})


def post_new(request):
    """Return page for adding new Post."""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'main/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    """View is for editing post."""
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'main/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    """Return draft list."""
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'main/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, pk):
    """View for publishing post."""
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def post_remove(request, pk):
    """View for deleting posts."""
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')
