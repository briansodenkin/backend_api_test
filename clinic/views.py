from rest_framework import mixins, viewsets

from clinic import serializers
from clinic.models import Clinic, Phone


class ClinicViewSet(viewsets.ModelViewSet):
    """View for the Clinic model."""

    serializer_class = serializers.ClinicDetailSerializer
    queryset = Clinic.objects.all()

    def get_queryset(self):
        """Get the list of clinics."""
        return self.queryset.order_by("-clinic_id")

    def get_serializer_class(self):
        """Get the correct serializers."""
        if self.action == "list":
            return serializers.ClinicSerializer
        return self.serializer_class


class PhoneViewSet(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Manage phone in the database."""

    serializer_class = serializers.PhoneSerializer
    queryset = Phone.objects.all()
