from rest_framework import viewsets

from district import serializers
from district.models import District


class DistrictViewSet(viewsets.ModelViewSet):
    """View for the District model."""

    serializer_class = serializers.DistrictSerializer
    queryset = District.objects.all()

    def get_queryset(self):
        """Get the list of districts"""
        return self.queryset.order_by("-district_id")
