from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the api accessible to the public"""

    def setUp(self):
        self.client = APIClient()


    def test_create_user_from_endpoint(self):
        """Test that user is create successfully"""

        payload = {
            'email': 'HighFaggot@gmail.com',
            'password': 'Dumrich!23',
            'name': 'Abhi'


        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**res.data)

        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a duplicate User fails"""
        payload = {'email': 'abhinavchavali23@gmail.com', 'password': 'Dumrich!23'}

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test if password is too short"""
        payload = {'email': 'abhinavchavali23@gmail.com', 'password': 'Hi'}

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_user(self):
        payload = {'email': 'abhinavhcvali12@gmail.com', 'password': 'testpass'}

        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test token is not created if cred. is not real"""
        create_user(email="test@londonappdev.com", password='Wrongh')
        payload = {'email':"test@londonapv.com", 'password':'Wronghss'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """If no user, no token"""
        payload = {'email':"test@londonapv.com", 'password':'Wronghss'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(email='abhinavchavali9205@gmil.com', password='noneYoBeesWax', name='Anjdf')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
