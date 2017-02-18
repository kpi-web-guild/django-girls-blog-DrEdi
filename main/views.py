"""All views are here."""
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required


def post_list(request):
    """Show all your Post objects."""
    posts = Post.objects.filter(published_date__lte=timezone.now())
    return render(request, 'main/index.html', {'posts': posts})


def post_detail(request, pk):
    """Show info about one post you have chosen."""
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'main/post_detail.html', {'post': post})


@login_required
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


def add_comment_to_post(request, pk):
    """If someone wants to create new comment he/she get this view."""
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'main/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    """Moderate comment."""
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    """Remove comment."""
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)
