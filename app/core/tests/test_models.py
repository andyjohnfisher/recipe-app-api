from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@a.co.uk', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


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

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
           user=sample_user(),
           name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
           user=sample_user(),
           name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_reipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
           user=sample_user(),
           title='Steak and mushroom sauce',
           time_minutes=5,
           price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_filename_uid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        expected_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, expected_path)
