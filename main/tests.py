"""Tests are here."""
from django.contrib.auth.models import User
from django.test import TestCase, Client
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
        del self.test_post


class ViewsTest(TestCase):
    """Testing class for views."""

    def setUp(self):
        """Prepare data for testing."""
        self.client = Client()
        self.admin = User.objects.create(username='testuser', password='blablabla', is_superuser=True, is_staff=True,
                                         email='testuser@gmail.com', is_active=True)

    def test_Index_view(self):
        """Testing main page."""
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)

    def test_detail_view(self):
        """Testing detail page when post is not exist and when it exists."""
        response = self.client.get('/post/1/')
        self.assertEqual(404, response.status_code)
        Post.objects.create(author=self.admin, title='Test', text='superText', created_date=timezone.now())
        response = self.client.get('/post/1/')
        self.assertEqual(200, response.status_code)

    def test_post_new_view(self):
        """Testing new post view before and after login."""
        response = self.client.get('/post/new/')
        self.assertEqual(302, response.status_code)
        authorization = self.client.login(username='admin', password='12345678')
        self.assertTrue(authorization)
        response = self.client.post('/post/new/', {'author': self.admin, 'title': 'Test', 'text': 'superText',
                                                   'created_date': timezone.now()}, follow=True)
        self.assertEqual(200, response.status_code)
        # Here's we have redirect_chain[0][0] because it's return list of tuples. We had only one redirect
        # so our list has only 1 element, tuple has 2 - first it's a link where we were redirected and second
        # it's a status code
        self.assertEqual('/post/1/', response.redirect_chain[0][0])

    def test_post_edit(self):
        """Testing edit views before and after user login."""
        response = self.client.get('/post/1/edit/')
        self.assertEqual(302, response.status_code)
        authorization = self.client.login(username='admin', password='12345678')
        self.assertTrue(authorization)
        response = self.client.get('/post/1/edit/')
        # This time we'are logged but post is not exist
        self.assertEqual(404, response.status_code)
        Post.objects.create(author=self.admin, title='Test', text='superText', created_date=timezone.now())
        response = self.client.get('/post/1/edit/')
        self.assertEqual(200, response.status_code)

    def test_drafts(self):
        """Testing drafts view before and after login."""
        response = self.client.get('/drafts/')
        self.assertEqual(302, response.status_code)
        authorization = self.client.login(username='admin', password='12345678')
        self.assertTrue(authorization)
        response = self.client.get('/drafts/')
        self.assertEqual(200, response.status_code)

    def test_publish_post(self):
        """Testing publishing post before login and after."""
        response = self.client.get('/post/1/publish/')
        self.assertEqual(302, response.status_code)
        authorization = self.client.login(username='admin', password='12345678')
        self.assertTrue(authorization)
        response = self.client.get('/post/1/publish/')
        self.assertEqual(404, response.status_code)
        Post.objects.create(author=self.admin, title='Test', text='superText', created_date=timezone.now())
        response = self.client.get('/post/1/publish/', follow=True)
        # The same situation as with new post test
        self.assertEqual(response.redirect_chain[0][0], '/post/1/')

    def test_delete_post(self):
        """Testing deleting post before and after login."""
        response = self.client.get('/post/1/remove/')
        self.assertEqual(302, response.status_code)
        authorization = self.client.login(username='admin', password='12345678')
        self.assertTrue(authorization)
        response = self.client.get('/post/1/remove/')
        self.assertEqual(404, response.status_code)
        Post.objects.create(author=self.admin, title='Test', text='superText', created_date=timezone.now())
        response = self.client.get('/post/1/remove/', follow=True)
        self.assertEqual('/', response.redirect_chain[0][0])

    def test_add_comment(self):
        """Add comment to post."""
        self.post = Post.objects.create(author=self.admin, title='Test', text='superText', created_date=timezone.now())
        resqonse = self.client.get('/post/1/comment/')
        self.assertEqual(200, resqonse.status_code)
        response = self.client.post('/post/1/comment/', {'author': self.admin, 'text': 'Super',
                                                         'created_date': timezone.now(), 'is_approved': False},
                                    follow=True)
        self.assertEqual('/post/1/', response.redirect_chain[0][0])

    def test_comment_aprove(self):
        """Testing comment approve view."""
        self.post = Post.objects.create(author=self.admin, title='Test', text='superText', created_date=timezone.now())
        self.comment = Comment.objects.create(post=self.post, author=self.admin, text='superComment',
                                              created_date=timezone.now(), is_approved=False)
        authorization = self.client.login(username='admin', password='12345678')
        self.assertTrue(authorization)
        response = self.client.get('/comment/1/approve/', follow=True)
        self.assertEqual('/post/1/', response.redirect_chain[0][0])

    def test_comment_delete(self):
        """Testing delete comment view."""
        self.post = Post.objects.create(author=self.admin, title='Test', text='superText', created_date=timezone.now())
        self.comment = Comment.objects.create(post=self.post, author=self.admin, text='superComment',
                                              created_date=timezone.now(), is_approved=False)
        authorization = self.client.login(username='admin', password='12345678')
        self.assertTrue(authorization)
        response = self.client.get('/comment/1/remove/', follow=True)
        self.assertEqual('/post/1/', response.redirect_chain[0][0])

    def tearDown(self):
        """Clean data after each test."""
        del self.client
