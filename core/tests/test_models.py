from django.contrib.auth import get_user_model
from django.test import TestCase

from clinic.models import Clinic, Phone
from district.models import District
from doctor.models import Category, Doctor


class ModelTests(TestCase):
    """Test Customized User model"""

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

    def test_create_district(self):
        """Test district model can be created."""
        district = District.objects.create(
            district_name="dummy",
        )
        self.assertEqual(str(district), district.district_name)

    def test_create_clinic(self):
        """Test clinic model can be created."""
        district = District.objects.create(
            district_name="dummy",
        )
        clinic = Clinic.objects.create(
            clinic_name="Dummy clinic",
            clinic_address="Dummy address",
            district=district,
        )
        self.assertEqual(str(clinic), clinic.clinic_name)

    def test_create_phone(self):
        """Test phone model can be created."""
        district = District.objects.create(
            district_id=19,
            district_name="dummy",
        )
        clinic = Clinic.objects.create(
            clinic_name="Dummy clinic",
            clinic_address="Dummy address",
            district=district,
        )
        phone = Phone.objects.create(
            phone_number=12345678,
            clinic=clinic,
        )
        self.assertEqual(str(phone), str(phone.phone_number))

    def test_create_doctor(self):
        """Test creating a Doctor is successful."""
        district = District.objects.create(
            district_id=19,
            district_name="dummy",
        )
        clinic = Clinic.objects.create(
            clinic_name="Dummy clinic",
            clinic_address="Dummy address",
            district=district,
        )
        category = Category.objects.create(category_name="Dummy")
        doctor = Doctor.objects.create(
            first_name="Dummy First Name",
            last_name="Dummy Last Name",
            price=12123,
            price_description="Dummy price",
            exclu_price=12323,
            availability={
                "monday": "1000 - 1700",
                "Tuesday": "1100 - 1800",
            },
            language=1,
        )
        doctor.category.add(category)
        doctor.clinic.add(clinic)
        doctor.save()
        self.assertEqual(str(doctor), doctor.first_name + doctor.last_name)

    def test_create_category(self):
        """Test creating a Category is successful."""
        category = Category.objects.create(category_name="Dummy")

        self.assertEqual(str(category), category.category_name)
