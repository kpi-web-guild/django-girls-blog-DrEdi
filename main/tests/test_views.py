"""Tests for views are at this file."""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

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

    def test_index_view(self):
        """Testing main page."""
        post = Post.objects.create(author=self.user, title='Test', text='superText')
        post.publish()
        response = self.client.get(reverse('post_list'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'main/index.html')
        self.assertContains(response, 'Test')

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
