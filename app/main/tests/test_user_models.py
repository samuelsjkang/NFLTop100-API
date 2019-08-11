from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTests(TestCase):
    '''Tests creation of new user'''
    def test_create_user(self):
        email = 'user@gmail.com'
        pw = 'password'
        user = User.objects.create_user(
            email=email,
            password=pw
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(pw))

    '''Tests that email for a user is normalized'''
    def test_normalized_email(self):
        email = 'user@GmAiL.cOm'
        user = User.objects.create_user(
            email,
            'password'
        )
        self.assertEqual(user.email, email.lower())

    '''Tests that user creation requires email'''
    def test_email_present(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(None, 'password')

    '''Tests superuser creation'''
    def test_create_superuser(self):
        user = User.objects.create_superuser(
            'sam@gmail.com',
            'password'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
