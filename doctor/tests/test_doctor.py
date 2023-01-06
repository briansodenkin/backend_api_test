from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers, status
from rest_framework.test import APIClient

from clinic.models import Clinic, Phone
from district.models import District
from doctor.models import Category, Doctor
from doctor.serializers import DoctorDetailSerializer, DoctorSerializer

DOCTOR_URL = reverse("doctor:doctor-list")


def detail_url(doctor_id):
    """Create and return a Doctor detail URL."""
    return reverse("doctor:doctor-detail", args=[doctor_id])


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


def create_category():
    """Create the category."""
    category = Category.objects.create(category_name="Dummy")
    return category


def create_doctor(**params):
    """Create and return a sample Doctor."""
    defaults = {
        "first_name": "dummy",
        "last_name": "dummy",
        "price": 1200,
        "price_description": "Body Checking",
        "exclu_price": 1000,
        "availability": {"monday": "1000-1800"},
        "language": 1,
    }

    doctor = Doctor.objects.create(**defaults)
    doctor.category.add(params["category"])
    doctor.clinic.add(params["clinic"])
    doctor.save()
    return doctor


class DoctorTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_get_doctors(self):
        """Test retrieving a list of Doctor."""

        res = self.client.get(DOCTOR_URL)
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for doctor in res.data:
            self.assertIn(doctor, serializer.data)

    def test_get_doctor_detail(self):
        """Test get Doctor detail."""
        district = create_district()
        category_1 = create_category()
        clinic_1 = create_clinic(address="Dummy address 1", district=district)
        doctor = create_doctor(category=category_1, clinic=clinic_1)

        url = detail_url(doctor.doctor_id)
        res = self.client.get(url)

        serializer = DoctorDetailSerializer(doctor)
        self.assertEqual(res.data, serializer.data)

    def test_create_doctor(self):
        """Test creating a Doctor."""
        create_category()
        district = create_district()
        create_clinic(address="Dummy address 1", district=district)
        defaults = {
            "first_name": "dummy",
            "last_name": "dummy",
            "price": 1200,
            "price_description": "Body Checking",
            "exclu_price": 1000,
            "availability": {"monday": "1000-1800"},
            "language": 1,
            "category": [{"category_id": 2, "category_name": "Dummy 1"}],
            "clinic": [
                {
                    "clinic_id": 11,
                    "clinic_name": "Dummy clinic",
                    "clinic_address": "Dummy address 2",
                    "district": 10,
                    "phone_clinic": [],
                }
            ],
        }
        res = self.client.post(DOCTOR_URL, defaults, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        doctor = Doctor.objects.get(doctor_id=res.data["doctor_id"])
        for k, v in defaults.items():
            if not (k in ["category", "clinic"]):
                self.assertEqual(getattr(doctor, k), v)

    def test_create_user_with_invalid_price_returns_error(self):
        """Test create with invalid price."""
        create_category()
        district = create_district()
        create_clinic(address="Dummy address 1", district=district)
        defaults = {
            "first_name": "dummy",
            "last_name": "dummy",
            "price": 120000000,
            "price_description": "Body Checking",
            "exclu_price": 10000000,
            "availability": {"monday": "1000-1800"},
            "language": 1,
            "category": [{"category_id": 2, "category_name": "Dummy 1"}],
            "clinic": [
                {
                    "clinic_id": 11,
                    "clinic_name": "Dummy clinic",
                    "clinic_address": "Dummy address 2",
                    "district": 10,
                    "phone_clinic": [],
                }
            ],
        }
        res = self.client.post(DOCTOR_URL, defaults, format="json")
        self.assertEqual(res.status_code, 400)
        self.assertRaises(serializers.ValidationError)

    def test_create_user_with_invalid_name_returns_error(self):
        """Test create with invalid price."""
        create_category()
        district = create_district()
        create_clinic(address="Dummy address 1", district=district)
        defaults = {
            "first_name": "",
            "last_name": "",
            "price": 1200,
            "price_description": "Body Checking",
            "exclu_price": 1000,
            "availability": {"monday": "1000-1800"},
            "language": 1,
            "category": [{"category_id": 2, "category_name": "Dummy 1"}],
            "clinic": [
                {
                    "clinic_id": 11,
                    "clinic_name": "Dummy clinic",
                    "clinic_address": "Dummy address 2",
                    "district": 10,
                    "phone_clinic": [],
                }
            ],
        }
        res = self.client.post(DOCTOR_URL, defaults, format="json")
        self.assertEqual(res.status_code, 400)
        self.assertRaises(serializers.ValidationError)

    def test_partial_update_doctor(self):
        """Test partial update of a Doctor."""
        district = create_district()
        category_1 = create_category()
        clinic_1 = create_clinic(address="Dummy address 1", district=district)
        doctor = create_doctor(category=category_1, clinic=clinic_1)
        payload = {"first_name": "New Name"}
        url = detail_url(doctor.doctor_id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        doctor.refresh_from_db()
        self.assertEqual(doctor.first_name, payload["first_name"])

    def test_full_update_doctor(self):
        """Test full update of Doctor."""
        district = create_district()
        category_1 = create_category()
        clinic_1 = create_clinic(address="Dummy address 1", district=district)
        doctor = create_doctor(category=category_1, clinic=clinic_1)

        payload = {
            "first_name": "dummy",
            "last_name": "dummy",
            "price": 1200,
            "price_description": "Body Checking",
            "exclu_price": 1000,
            "availability": {"monday": "1000-1800"},
            "language": 1,
            "category": [{"category_id": 2, "category_name": "Dummy 1"}],
            "clinic": [
                {
                    "clinic_id": 11,
                    "clinic_name": "Dummy clinic",
                    "clinic_address": "Dummy address 2",
                    "district": 10,
                    "phone_clinic": [],
                }
            ],
        }
        url = detail_url(doctor.doctor_id)
        res = self.client.put(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        doctor.refresh_from_db()
        for k, v in payload.items():
            if not (k in ["category", "clinic"]):
                self.assertEqual(getattr(doctor, k), v)
