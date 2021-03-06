"""Models for your project are located here."""
from django.db import models
from django.utils import timezone


class Post(models.Model):
    """Model that represents post in our blog."""

    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        """Publishing post."""
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        """Return title of Post.

        This is used when rendering model instance as a string
        """
        return self.title

    @property
    def approved_comments(self):
        """Show comments that are ok in user's opinion."""
        return self.comments.filter(approved_comment=True)


class Comment(models.Model):
    """Model for comments."""

    post = models.ForeignKey('main.Post', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=False)

    def approve(self):
        """Approve comment and save it in DB."""
        self.is_approved = True
        self.save()

    def __str__(self):
        """Render Comment instance as its text by default when stringifying."""
        return self.text
