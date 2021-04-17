from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from .models import Post
import json

User = get_user_model()
class PostTestCase(TestCase):
    def setUp(self):
        user_a = User(username='abc', email='abc@invalid.com')
        user_a_pass = 'some_123pass'
        self.user_a_pass = user_a_pass
        user_a.is_staff = True
        user_a.is_superuser = False
        user_a.set_password(user_a_pass)
        user_a.save()
        self.user_a = user_a
        user_b = User.objects.create_user('abc2', 'abc2@invalid.com', 'passwordtest')
        self.user_b = user_b
    
    def test_user_count(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 2)
    
    def test_valid_request(self):
        self.client.login(username=self.user_a.username, password='some_123pass')
        response = self.client.post(reverse('post-create'), {"title": "title", "content":"content"}, follow=True)
        self.assertEqual(response.status_code, 200)

class BlogViewsTestCase(TestCase):
    
    def setUp(self):
        self.user_1 = User.objects.create_user('abc', 'abc@invalid.com', 'passwordtest')
        self.post_1 = Post.objects.create(title='post', content='content', author=self.user_1)

    def test_home_view(self):
        response = self.client.get(reverse('blog-home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')
    
    def test_user_post_list_view(self):
        response = self.client.get(reverse('user-posts', args=[self.user_1.username]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/user_posts.html')
    
    def test_post_detail_view(self):
        response = self.client.get(reverse('post-detail', args=[self.post_1.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
    
    def test_post_create_view(self):
        self.client.login(username=self.user_1.username, password='passwordtest')
        response = self.client.get(reverse('post-create'), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_form.html')
    
    def test_post_update_view(self):
        self.client.login(username=self.user_1.username, password='passwordtest')
        response = self.client.get(reverse('post-update', args=[self.post_1.id]), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_form.html')

    def test_post_delete_view(self):
        self.client.login(username=self.user_1.username, password='passwordtest')
        response = self.client.get(reverse('post-delete', args=[self.post_1.id]), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_confirm_delete.html')

    def test_home_view(self):
        response = self.client.get(reverse('blog-about'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/about.html')


