"""Tests are here."""
from django.contrib.auth.models import User
from django.test import TestCase
from datetime import datetime

from main.models import Post, Comment
# Create your tests here.


class ModelTest(TestCase):
    """Main class for testing models of this project."""

    def setUp(self):
        """Prepare data for testing."""
        self.admin = User.objects.create(username='testuser')
        self.test_post = Post.objects.create(author=self.admin, title='Test', text='superText',
                                             created_date=datetime.now())
        self.comment = Comment.objects.create(post=self.test_post, author=self.admin, text='superComment',
                                              created_date=datetime.now(), is_approved=False)

    def test_Post_str(self):
        """Magic method __str__ working okay."""
        self.assertEqual(str(self.test_post), self.test_post.title)

    def test_Post_is_publish_method(self):
        """Publish method working ok."""
        self.assertIsNone(self.test_post.published_date)
        self.test_post.publish()
        self.assertIsNotNone(self.test_post.published_date)

    def test_Comment_str(self):
        """Magic method str working ok."""
        self.assertEqual(str(self.comment), self.comment.text)
