"""
URL mappings for the Clinic app.
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from doctor import views

router = DefaultRouter()
router.register("", views.DoctorViewSet)


app_name = "doctor"

urlpatterns = [
    path("", include(router.urls)),
]
