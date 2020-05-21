from django.test import TestCase

from calc import add   # works
# from app.calc import add # fails
from calc import subtract


class CalcTests(TestCase):

    def test_add_numbers(self):
        """Test that 2 numbers are added together"""
        self.assertEqual(add(3, 8), 11)

    def test_subtract_numbers(self):
        """Test that values are subtrated and returned"""
        self.assertEqual(subtract(5, 11), 6)
