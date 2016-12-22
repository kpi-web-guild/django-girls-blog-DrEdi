"""Management of admin panel.

Here we add models to admin panel and after manage it from our site
You can register it or if you want change some setting, hot to show
what info you want to see on display about this model
"""
from django.contrib import admin
from .models import Post, Comment

admin.site.register(Post)
admin.site.register(Comment)
