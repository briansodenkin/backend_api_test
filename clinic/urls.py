"""
URL mappings for the Clinic app.
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from clinic import views

router = DefaultRouter()
router.register("", views.ClinicViewSet)


app_name = "clinic"

urlpatterns = [
    path("", include(router.urls)),
]
