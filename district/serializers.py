from rest_framework import serializers

from district.models import District


class DistrictSerializer(serializers.ModelSerializer):
    """Serializer for districts."""

    class Meta:
        model = District
        fields = [
            "district_id",
            "district_name",
        ]
