from django.test import TestCase

from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_sucessful(self):
        """Test creating a new user with an email"""
        email = 'test@frog.co.uk'
        pw = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=pw
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(pw))

    def test_new_user_email_normalised(self):
        """Test the email for a new user gets normalised"""
        email = 'test@FROGS.CO.UK'
        user = get_user_model().objects.create_user(email, 'abc')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email cases error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'abc')

    def test_create_new_supperuser(self):
        """Test creating a new supper user"""
        user = get_user_model().objects.create_superuser(
            'test@abc.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
