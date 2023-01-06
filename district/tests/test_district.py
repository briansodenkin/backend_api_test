from collections import OrderedDict

from django.test import TestCase

from district.models import District
from district.serializers import DistrictSerializer


def create_district(**params):
    """Create and return a sample district."""
    defaults = {
        "district_name": "Dummy",
    }
    defaults.update(params)

    district = District.objects.create(**defaults)

    return district


class DistrictTests(TestCase):
    """Test the public API requests for District."""

    def test_get_district(self):
        """Test get all the list of districts."""
        create_district()
        create_district(district_name="Dummy 2")
        districts = District.objects.all()
        serializer = DistrictSerializer(districts, many=True)
        expected_districts = [
            OrderedDict([("district_id", 1), ("district_name", "Central and Western")]),
            OrderedDict([("district_id", 2), ("district_name", "Eastern")]),
            OrderedDict([("district_id", 3), ("district_name", "Southern")]),
            OrderedDict([("district_id", 4), ("district_name", "Wan Chai")]),
            OrderedDict([("district_id", 5), ("district_name", "Kowloon City")]),
            OrderedDict([("district_id", 6), ("district_name", "Kwun Tong")]),
            OrderedDict([("district_id", 7), ("district_name", "Sham Shui Po")]),
            OrderedDict([("district_id", 8), ("district_name", "Wong Tai Sin")]),
            OrderedDict([("district_id", 9), ("district_name", "Yau Tsim Mong")]),
            OrderedDict([("district_id", 10), ("district_name", "Dummy")]),
            OrderedDict([("district_id", 11), ("district_name", "Dummy 2")]),
        ]
        self.assertEqual(expected_districts, serializer.data)

    def test_get_district_by_district_name(self):
        """Test get all the list of districts."""
        create_district()
        district = District.objects.filter(district_name="Dummy").first()
        serializer = DistrictSerializer(district)
        expected_district = {"district_id": 10, "district_name": "Dummy"}
        self.assertEqual(expected_district, serializer.data)
