"""All models are here."""
from django.db import models
from django.utils import timezone

# Create your models here.


class Post(models.Model):
    """Model that represent post in our blog."""

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
        """Return title of post."""
        return self.title
