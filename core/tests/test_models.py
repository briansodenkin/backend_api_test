from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test Customized User model
    """

    def test_create_user_with_email(self):
        """Test user can be created successfully"""
        email = "test@dummy.com"
        password = "dummy123"
        user = get_user_model().objects.create_user(email=email, password=password)
        # print(user)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test if the email is normalized"""
        sample_emails = [
            ("test2@DUMMy.com", "test2@dummy.com"),
            ("test3@Dummy.com", "test3@dummy.com"),
        ]
        for text in sample_emails:
            raw_text, normalized_text = text
            user = get_user_model().objects.create_user(
                email=raw_text, password="dummy123"
            )
            self.assertEqual(user.email, normalized_text)

    def test_new_user_without_email(self):
        """Test error is raised when no email is provided"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "dummy123")

    def test_create_superuser(self):
        """Test superuser can be created"""
        user = get_user_model().objects.create_superuser("test@dummy.com", "dummy123")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
