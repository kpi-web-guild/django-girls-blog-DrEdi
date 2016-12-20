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

        This is useful if you need to get info only about title of Post object
        """
        return self.title

    def approved_comments(self):
        """Approving comments. Use for moderating."""
        return self.comments.filter(approved_comment=True)


class Comment(models.Model):
    """Model for comments."""

    post = models.ForeignKey('main.Post', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        """Approve comment and save it in DB."""
        self.approved_comment = True
        self.save()

    def __str__(self):
        """Render Comment instance as it's text by default when stringifying."""
        return self.text
