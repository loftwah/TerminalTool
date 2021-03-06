from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with email"""
        email = 'test@gmail.com'
        password = 'testpass123'

        user = get_user_model().objects.create_user(

            email=email,
            password=password

            )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):

        email = "test@GMAIL.COM"
        user = get_user_model().objects.create_user(

            email=email,
            password="NIrma"

            )
        print(user.email.lower())

        self.assertEqual(user.email, email.lower())

    def test_create_superuser(self):
        """Create a superuser"""
        user = get_user_model().objects.create_superuser("dumrich@gmail.com", 'Dumrich!23')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
