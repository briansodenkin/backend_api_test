from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")


def create_user(**params):
    """Create and reture an new user."""

    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the api for user works"""

    def setUp(self):
        payload = {
            "email": "test@dummy.com",
            "password": "dummy123",
            "name": "Dummy",
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_valid(self):
        """Test if the checking for the password works"""
        payload = {
            "email": "test@dummy.com",
            "password": "d",
            "name": "Dummy",
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)

    def test_create_token(self):
        """Test if token is generated."""
        credentials = {
            "name": "Dummy",
            "email": "test@dummy.com",
            "password": "dummy123",
        }
        create_user(**credentials)
        payload = {
            "email": credentials["email"],
            "password": credentials["password"],
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test error raised if invalid credentials."""
        create_user(email="test@dummy.com", password="dummy123")
        payload = {"email": "test@dummy.com", "password": "dummy123"}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_credentials(self):
        """Test error raised if blank credentials."""
        payload = {"email": "test@dummy.com", "password": ""}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
