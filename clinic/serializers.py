from rest_framework import serializers

from clinic.models import Clinic, Phone


class PhoneSerializer(serializers.ModelSerializer):
    """Serializer for phone."""

    class Meta:
        model = Phone
        fields = [
            "phone_id",
            "phone_number",
            "clinic",
        ]


class ClinicSerializer(serializers.ModelSerializer):
    """Serializer for clinic."""

    phone_clinic = serializers.SerializerMethodField()

    class Meta:
        model = Clinic
        fields = [
            "clinic_id",
            "clinic_name",
            "clinic_address",
            "district",
            "phone_clinic",
        ]

    def get_phone_clinic(self, obj):
        phone_clinic = Phone.objects.filter(clinic=obj.clinic_id)
        serializer = PhoneSerializer(phone_clinic, many=True)

        return serializer.data


class ClinicDetailSerializer(ClinicSerializer):
    """Serializer detail clinic."""

    class Meta:
        model = Clinic
        fields = ClinicSerializer.Meta.fields
