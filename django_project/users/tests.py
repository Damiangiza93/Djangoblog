from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings


User = get_user_model()
class UserTestCase(TestCase):

    def setUp(self):
        user_a = User(username='abc', email='abc@invalid.com')
        user_a_pass = 'some_123pass'
        self.user_a_pass = user_a_pass
        user_a.is_staff = True
        user_a.is_superuser = True
        user_a.set_password(user_a_pass)
        user_a.save()
        self.user_a = user_a

    def test_user_exists(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 1)
        self.assertNotEqual(user_count, 0)

    def test_user_password(self):
        self.assertTrue(self.user_a.check_password(self.user_a_pass))

    def test_login_url(self):
        login_url = settings.LOGIN_URL
        data = {"username": "abc", "password": self.user_a_pass}
        response = self.client.post(reverse('login'), data, follow=True)
        status_code = response.status_code
        redirect_path = response.request.get("PATH_INFO")
        self.assertEqual(status_code, 200)
