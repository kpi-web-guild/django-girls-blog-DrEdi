"""Tests for views are at this file."""
from unittest.mock import patch
from datetime import datetime

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone

from main.models import Post, Comment


class ViewsTest(TestCase):
    """Testing class for views."""

    USERNAME = 'admin'
    PASSWORD = '12345678'

    def setUp(self):
        """Prepare data for testing."""
        self.client = Client()
        self.user = User.objects.create(username='testuser', password='blablabla', is_superuser=True, is_staff=True,
                                        email='testuser@gmail.com', is_active=True)

    def test_index_view_rendering(self):
        """Testing main page for render needed posts."""
        tz = timezone.get_current_timezone()
        post = Post.objects.create(author=self.user, title='Test', text='superText',
                                   created_date=datetime(day=1, month=3, year=2016, tzinfo=tz),
                                   published_date=datetime(day=1, month=3, year=2016, tzinfo=tz))
        past_post = Post.objects.create(author=self.user, title='past_est', text='superText',
                                        created_date=datetime(day=1, month=4, year=2015, tzinfo=tz),
                                        published_date=datetime(day=1, month=4, year=2015, tzinfo=tz))
        future_post = Post.objects.create(author=self.user, title='future_test', text='superText',
                                          created_date=datetime(day=1, month=4, year=2116, tzinfo=tz),
                                          published_date=datetime(day=1, month=4, year=2116, tzinfo=tz))
        with patch('django.utils.timezone.now', lambda: datetime(day=1, month=1, year=2016, tzinfo=tz)):
            response = self.client.get(reverse('post_list'))
            self.assertContains(response, past_post)
            self.assertNotContains(response, post)
            self.assertNotContains(response, future_post)
        with patch('django.utils.timezone.now', lambda: datetime(day=1, month=4, year=2016, tzinfo=tz)):
            response = self.client.get(reverse('post_list'))
            self.assertContains(response, past_post)
            self.assertContains(response, post)
            self.assertNotContains(response, future_post)
        with patch('django.utils.timezone.now', lambda: datetime(day=1, month=4, year=3016, tzinfo=tz)):
            response = self.client.get(reverse('post_list'))
            self.assertContains(response, past_post.title)
            self.assertContains(response, post)
            self.assertContains(response, future_post)
        response = self.client.get(reverse('post_list'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'main/index.html')
        self.assertListEqual(list(response.context['posts']), [post, past_post])

    def test_detail_view(self):
        """Testing detail page when post is not exist and when it exists."""
        response = self.client.get(reverse('post_detail', kwargs={'pk': 1}))
        self.assertEqual(404, response.status_code)
        post = Post.objects.create(author=self.user, title='Test', text='superText')
        response = self.client.get(reverse('post_detail', kwargs={'pk': post.pk}))
        self.assertEqual(200, response.status_code)

    def test_post_new_view(self):
        """Testing new post view before and after login."""
        response = self.client.get(reverse('post_new'))
        self.assertEqual(302, response.status_code)
        authorization = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertTrue(authorization)
        response = self.client.post(reverse('post_new'), {'author': self.user, 'title': 'Test', 'text': 'superText', },
                                    follow=True)
        self.assertEqual(200, response.status_code)
        self.assertRedirects(response, reverse('post_detail', kwargs={'pk': 1}))

    def test_post_edit(self):
        """Testing edit views before and after user login."""
        response = self.client.get(reverse('post_edit', kwargs={'pk': 1}))
        self.assertEqual(302, response.status_code)
        authorization = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertTrue(authorization)
        response = self.client.get(reverse('post_edit', kwargs={'pk': 1}))
        # This time we'are logged but post is not exist
        self.assertEqual(404, response.status_code)
        post = Post.objects.create(author=self.user, title='Test', text='superText')
        response = self.client.get(reverse('post_edit', kwargs={'pk': post.pk}))
        self.assertEqual(200, response.status_code)

    def test_drafts(self):
        """Testing drafts view before and after login."""
        response = self.client.get(reverse('post_draft_list'))
        self.assertEqual(302, response.status_code)
        authorization = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertTrue(authorization)
        response = self.client.get(reverse('post_draft_list'))
        self.assertEqual(200, response.status_code)

    def test_publish_post(self):
        """Testing publishing post before login and after."""
        response = self.client.get(reverse('post_publish', kwargs={'pk': 1}))
        self.assertEqual(302, response.status_code)
        authorization = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertTrue(authorization)
        response = self.client.get(reverse('post_publish', kwargs={'pk': 1}))
        self.assertEqual(404, response.status_code)
        post = Post.objects.create(author=self.user, title='Test', text='superText')
        response = self.client.get(reverse('post_publish', kwargs={'pk': post.pk}), follow=True)
        self.assertRedirects(response, reverse('post_detail', kwargs={'pk': post.pk}))

    def test_delete_post(self):
        """Testing deleting post before and after login."""
        response = self.client.get(reverse('post_remove', kwargs={'pk': 1}))
        self.assertEqual(302, response.status_code)
        authorization = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertTrue(authorization)
        response = self.client.get(reverse('post_remove', kwargs={'pk': 1}))
        self.assertEqual(404, response.status_code)
        post = Post.objects.create(author=self.user, title='Test', text='superText')
        response = self.client.get(reverse('post_remove', kwargs={'pk': post.pk}), follow=True)
        self.assertRedirects(response, reverse('post_list'))

    def test_add_comment(self):
        """Add comment to post."""
        self.post = Post.objects.create(author=self.user, title='Test', text='superText')
        response = self.client.get(reverse('add_comment_to_post', kwargs={'pk': self.post.pk}))
        self.assertEqual(200, response.status_code)
        response = self.client.post(reverse('add_comment_to_post', kwargs={'pk': self.post.pk}),
                                    {'author': self.user, 'text': 'Super'}, follow=True)
        self.assertRedirects(response, reverse('post_detail', kwargs={'pk': self.post.pk}))

    def test_comment_aprove(self):
        """Testing comment approve view."""
        self.post = Post.objects.create(author=self.user, title='Test', text='superText')
        self.comment = Comment.objects.create(post=self.post, author=self.user, text='superComment')
        authorization = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertTrue(authorization)
        response = self.client.get(reverse('comment_approve', kwargs={'pk': self.comment.pk}), follow=True)
        self.assertRedirects(response, reverse('post_detail', kwargs={'pk': self.post.pk}))

    def test_comment_delete(self):
        """Testing delete comment view."""
        self.post = Post.objects.create(author=self.user, title='Test', text='superText')
        self.comment = Comment.objects.create(post=self.post, author=self.user, text='superComment')
        authorization = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertTrue(authorization)
        response = self.client.get(reverse('comment_remove', kwargs={'pk': self.comment.pk}), follow=True)
        self.assertRedirects(response, reverse('post_detail', kwargs={'pk': self.post.pk}))

    def tearDown(self):
        """Clean data after each test."""
        del self.client
        del self.user
