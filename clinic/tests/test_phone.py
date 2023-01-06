from django.test import TestCase
from rest_framework.test import APIClient

from clinic.models import Clinic, Phone
from clinic.serializers import PhoneSerializer
from district.models import District


def create_district(**params):
    district = District.objects.create(
        district_name="dummy",
    )
    return district


def create_clinic(**params):
    """Create and return a sample clinic."""
    clinic = Clinic.objects.create(
        clinic_name="Dummy clinic",
        clinic_address=params["address"],
        district=params["district"],
    )

    return clinic


def create_phone(**params):
    """Create the phone number"""
    phone = Phone.objects.create(
        phone_number=params["phone_number"],
        clinic=params["clinic"],
    )
    return phone


class PhoneTests(TestCase):
    """Test the get functions of the clinic model."""

    def setUp(self):
        self.client = APIClient()

    def test_get_phone(self):
        """Test get all the list of phone."""
        district = create_district()
        clinic = create_clinic(address="Dummy address 1", district=district)
        create_phone(phone_number=12345678, clinic=clinic)
        create_phone(phone_number=12345679, clinic=clinic)
        phone = Phone.objects.all()
        serializer = PhoneSerializer(phone, many=True)
        res = self.client.get("http://127.0.0.1:8000/phone/")
        for i in res.data:
            self.assertIn(i, serializer.data)

    # Test for update, delete & create if api is exposed
