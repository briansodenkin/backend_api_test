"""
Serializers for Doctor APIs
"""
from rest_framework import serializers

from clinic.models import Clinic
from clinic.serializers import ClinicSerializer
from doctor.models import Category, Doctor


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category."""

    class Meta:
        model = Category
        fields = ["category_id", "category_name"]


class DoctorSerializer(serializers.ModelSerializer):
    """Serializer for Doctors."""

    category = CategorySerializer(many=True, required=False)
    clinic = ClinicSerializer(many=True, required=False)

    class Meta:
        model = Doctor
        fields = [
            "doctor_id",
            "first_name",
            "last_name",
            "price",
            "price_description",
            "exclu_price",
            "availability",
            "language",
            "category",
            "clinic",
        ]

    def _get_or_create_categories(self, categories, doctor):
        """Handle getting or creating categories as needed."""
        for category in categories:
            category_obj, created = Category.objects.get_or_create(
                **category,
            )
            doctor.category.add(category_obj)

    def _get_or_create_clinics(self, clinics, doctor):
        """Handle getting or creating clinics as needed."""
        for clinic in clinics:
            clinic_obj, created = Clinic.objects.get_or_create(
                **clinic,
            )
            doctor.clinic.add(clinic_obj)

    def create(self, validated_data):
        """Create a Doctor."""
        category = validated_data.pop("category", [])
        clinic = validated_data.pop("clinic", [])
        doctor = Doctor.objects.create(**validated_data)
        self._get_or_create_categories(category, doctor)
        self._get_or_create_clinics(clinic, doctor)

        return doctor

    def update(self, instance, validated_data):
        """Update Doctor."""
        category = validated_data.pop("category", None)
        clinic = validated_data.pop("clinic", None)
        if category is not None:
            instance.category.clear()
            self._get_or_create_categories(category, instance)
        if clinic is not None:
            instance.clinic.clear()
            self._get_or_create_clinics(clinic, instance)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class DoctorDetailSerializer(DoctorSerializer):
    """Serializer for Doctor detail view."""

    class Meta(DoctorSerializer.Meta):
        fields = DoctorSerializer.Meta.fields
