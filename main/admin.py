"""Admin panel code is here."""
from django.contrib import admin
from .models import Post
# Register your models here.
admin.site.register(Post)
