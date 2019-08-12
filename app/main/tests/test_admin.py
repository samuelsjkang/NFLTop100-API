from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

UserModel = get_user_model()


class AdminPageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = UserModel.objects.create_superuser(
            email='sam@gmail.com',
            password='password',
            name='Test Super'
        )
        self.client.force_login(self.admin_user)
        self.user = UserModel.objects.create_user(
            email='user@gmail.com',
            password='password',
            name='Test user'
        )

    # Tests that users are listed on the page
    def test_list_users(self):
        url = reverse('admin:main_user_changelist')
        res = self.client.get(url)
        self.assertContains(res, self.user.email)

    # Tests that user edit page loads
    def test_user_edit_page(self):
        url = reverse('admin:main_user_change', args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    # Tests that create user page loads
    def test_user_create_page(self):
        url = reverse('admin:main_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
