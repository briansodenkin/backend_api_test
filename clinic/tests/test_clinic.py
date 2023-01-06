from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from clinic.models import Clinic, Phone
from clinic.serializers import ClinicSerializer
from district.models import District

CLINIC_URL = reverse("clinic:clinic-list")


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
        phone_number=12345678,
        clinic=params["clinic"],
    )
    return phone


class ClinicTests(TestCase):
    """Test the get functions of the clinic model."""

    def setUp(self):
        self.client = APIClient()

    def test_get_clinic(self):
        """Test get all the list of districts."""
        district = create_district()
        create_clinic(address="Dummy address 1", district=district)
        res = self.client.get(CLINIC_URL)
        clinic = Clinic.objects.all()
        serializer = ClinicSerializer(clinic, many=True)
        for i in res.data:
            self.assertIn(i, serializer.data)

    def test_get_clinic_by_district(self):
        """Test get all the list of districts."""
        district = create_district()
        create_clinic(address="Dummy address 1", district=district)
        create_clinic(address="Dummy address 2", district=district)
        clinic = Clinic.objects.filter(district__district_name="dummy")
        serializer = ClinicSerializer(clinic, many=True)
        res = self.client.get(CLINIC_URL)
        for i in serializer.data:
            self.assertIn(i, res.data)

    def test_get_clinic_by_phone_number(self):
        """Test get all the list of districts."""
        district = create_district()
        clinic_1 = create_clinic(address="Dummy address 1", district=district)
        phone = create_phone(clinic=clinic_1)
        clinic_by_phone = Phone.objects.filter(
            phone_number=phone.phone_number
        ).values_list("clinic", flat=True)
        clinic = Clinic.objects.filter(clinic_id__in=clinic_by_phone)
        serializer = ClinicSerializer(clinic, many=True)
        res = self.client.get(CLINIC_URL)
        for i in serializer.data:
            self.assertIn(i, res.data)
