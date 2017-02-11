"""Tests for models."""
from unittest.mock import patch
from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from main.models import Post, Comment


class ModelTestPost(TestCase):
    """Main class for post testing models of this project."""

    def setUp(self):
        """Prepare data for testing."""
        self.user = User.objects.create(username='testuser')
        self.test_post = Post.objects.create(author=self.user, title='Test', text='superText',
                                             created_date=timezone.now())

    def test_post_rendering(self):
        """Post is rendered as its title."""
        self.assertEqual(str(self.test_post), self.test_post.title)

    @patch('django.utils.timezone.now', lambda: datetime(day=1, month=4, year=2016))
    def test_post_publish_method(self):
        """Publish method working ok."""
        self.test_post.publish()
        self.assertLess(self.test_post.published_date, datetime.now())
        self.assertEqual(self.test_post.published_date, datetime(day=1, month=4, year=2016))
        self.assertLess(datetime(day=1, month=4, year=2015), self.test_post.published_date)

    def tearDown(self):
        """Clean data for new test."""
        del self.user
        del self.test_post


class ModelTestComment(TestCase):
    """Main class for testing comment models of this project."""

    def setUp(self):
        """Prepare data for testing."""
        self.user = User.objects.create(username='testuser')
        self.test_post = Post.objects.create(author=self.user, title='Test', text='superText',
                                             created_date=timezone.now())
        self.comment = Comment.objects.create(post=self.test_post, author=self.user, text='superComment',
                                              created_date=timezone.now(), is_approved=False)

    def test_comment_rendering(self):
        """Comment is rendered as its title."""
        self.assertEqual(str(self.comment), self.comment.text)

    def tearDown(self):
        """Clean data for new test."""
        del self.user
        del self.test_post
        del self.comment
