from rest_framework import mixins, viewsets

from district.models import District
from doctor import serializers
from doctor.models import Category, Doctor


class DoctorViewSet(viewsets.ModelViewSet):
    """View for manage Doctor APIs."""

    serializer_class = serializers.DoctorDetailSerializer
    queryset = Doctor.objects.all()

    def _params_ints_to_ints(self, qs):
        """Convert a list of strings to integers."""
        return [int(str_id) for str_id in qs.split(",")]

    def _params_str_to_ints_categories(self, qs):
        """Convert a list of strings to integers."""
        return Category.objects.filter(category_name__in=qs.split(",")).values_list(
            "category_id", flat=True
        )

    def _params_str_to_ints_districts(self, qs):
        """Convert a list of strings to integers."""
        return District.objects.filter(district_name__in=qs.split(",")).values_list(
            "district_id", flat=True
        )

    def _params_str_to_ints_languages(self, qs):
        """Convert a list of strings to integers."""
        default_languages = {"english": 2, "chinese": 1}
        return [default_languages[param.lower()] for param in qs.split(",")]

    def _check_if_params_int(self, qs):
        return all(str(param).isdigit() for param in qs.split(","))

    def get_queryset(self):
        """Retrieve doctors."""
        categories = self.request.query_params.get("category")
        districts = self.request.query_params.get("district")
        language = self.request.query_params.get("language")
        queryset = self.queryset
        if categories:
            categories_ids = self._params_str_to_ints_categories(categories)
            if self._check_if_params_int(categories):
                categories_ids = self._params_ints_to_ints(categories)
            queryset = queryset.filter(category__category_id__in=categories_ids)
        if districts:
            districts_ids = self._params_str_to_ints_districts(districts)
            if self._check_if_params_int(districts):
                districts_ids = self._params_ints_to_ints(districts)
            queryset = queryset.filter(clinic__district__in=districts_ids)
        if language:
            language_id = self._params_str_to_ints_languages(language)
            if self._check_if_params_int(language):
                language_id = self._params_ints_to_ints(language)
            queryset = queryset.filter(language=language_id[0])
        return queryset.order_by("-doctor_id").distinct()

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == "list":
            return serializers.DoctorSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create Doctor."""
        serializer.save()


class CategoryViewSet(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Manage phone in the database."""

    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()
