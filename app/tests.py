from django.test import TestCase

# from calc import add   # works
from app.calc import add # fails


class CalcTests(TestCase):

    def test_add_numbers(self):
        """Test that 2 numbers are added together"""
        self.assertEqual(add(3, 8), 11)
