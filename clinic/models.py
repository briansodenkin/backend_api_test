from django.db import models

from district.models import District


class Clinic(models.Model):
    """Clinic object."""

    clinic_id = models.AutoField(primary_key=True)
    clinic_name = models.CharField(max_length=255)
    clinic_address = models.CharField(max_length=255, unique=True)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, related_name="district"
    )

    def __str__(self) -> str:
        return self.clinic_name


# One to Many relation
class Phone(models.Model):
    """Phone object."""

    phone_id = models.AutoField(primary_key=True)
    phone_number = models.SmallIntegerField()
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="clinic")

    def __str__(self) -> str:
        return str(self.phone_number)
