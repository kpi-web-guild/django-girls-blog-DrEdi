"""Tests for models."""
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from main.models import Post, Comment


class ModelTest(TestCase):
    """Main class for testing models of this project."""

    def setUp(self):
        """Prepare data for testing."""
        self.admin = User.objects.create(username='testuser')
        self.test_post = Post.objects.create(author=self.admin, title='Test', text='superText',
                                             created_date=timezone.now())

    def test_post_rendering(self):
        """Post is rendered as its title."""
        self.assertEqual(str(self.test_post), self.test_post.title)

    def test_post_publish_method(self):
        """Publish method working ok."""
        self.assertIsNone(self.test_post.published_date)
        self.test_post.publish()
        self.assertLessEqual(self.test_post.published_date, timezone.now())

    def test_comment_rendering(self):
        """Comment is rendered as its title."""
        self.comment = Comment.objects.create(post=self.test_post, author=self.admin, text='superComment',
                                              created_date=timezone.now(), is_approved=False)
        self.assertEqual(str(self.comment), self.comment.text)

    def tearDown(self):
        """Clean data for new test."""
        del self.admin