from django.db import models

from clinic.models import Clinic

LANGAUGE_CHOICES = ((1, "Chinese"), (2, "English"))


class Doctor(models.Model):
    """Doctor object."""

    doctor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    price = models.SmallIntegerField()
    price_description = models.TextField()
    exclu_price = models.SmallIntegerField()
    availability = models.JSONField()
    language = models.IntegerField(choices=LANGAUGE_CHOICES, default=1)
    category = models.ManyToManyField("Category")
    clinic = models.ManyToManyField(Clinic)

    def __str__(self) -> str:
        return self.first_name + self.last_name


# Many to Many relation
class Category(models.Model):
    """Category object."""

    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.category_name
