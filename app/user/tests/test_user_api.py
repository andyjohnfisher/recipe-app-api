from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
           'email': 'andy@b.com',
           'password': '12346',
           'name': 'me'
        }
        resp = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**resp.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', resp.data)

    def test_user_exists(self):
        """Test creating user that already exists fails"""
        payload = {
           'email': 'andy@b.com',
           'password': '123',
           'name': 'not me'
        }
        create_user(**payload)
        resp = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than 5 chars"""
        payload = {
           'email': 'andy2@b.com',
           'password': 'pw',
           'name': 'not me'
        }
        resp = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
           email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {
           'email': 'andy2@b.com',
           'password': 'pwpwpw',
           'name': 'not me'
        }
        create_user(**payload)
        resp = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials given"""
        payload = {
           'email': 'andy2@b.com',
           'password': 'pwpwpw',
           'name': 'not me'
        }
        create_user(**payload)
        payload['password'] = 'wrongpass'
        resp = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', resp.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user does not exist"""
        payload = {
           'email': 'andy2@b.com',
           'password': 'pwpwpw',
           'name': 'not me'
        }
        resp = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', resp.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        resp = self.client.post(TOKEN_URL, {'password': '', 'email': 'one'})

        self.assertNotIn('token', resp.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
