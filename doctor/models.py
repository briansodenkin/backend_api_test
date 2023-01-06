from django.db import models
from rest_framework import serializers

from clinic.models import Clinic

LANGAUGE_CHOICES = ((1, "Chinese"), (2, "English"))


def validate_name(input_name):
    if len(input_name) < 1:
        raise serializers.ValidationError("Invalid name: Empty string")


def validate_price(input_price):
    if input_price < 0:
        raise serializers.ValidationError("Invalid price: Negative value")
    if input_price > 1000000:
        raise serializers.ValidationError(
            "Invalid price: Price should be smaller than 1 Million"
        )


def validate_availability(value):
    if not isinstance(value, dict):
        raise serializers.ValidationError(
            "Invalid availablity: Availability should be in Dict"
        )
    if not all(
        k.lower()
        in [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]
        for k in value.keys()
    ):
        raise serializers.ValidationError(
            "Invalid availablity: Availability' keys from Monday to Friday"
        )


class Doctor(models.Model):
    """Doctor object."""

    doctor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255, validators=[validate_name])
    last_name = models.CharField(max_length=255, validators=[validate_name])
    price = models.SmallIntegerField(validators=[validate_price])
    price_description = models.TextField()
    exclu_price = models.SmallIntegerField(validators=[validate_price])
    availability = models.JSONField(validators=[validate_availability])
    language = models.IntegerField(choices=LANGAUGE_CHOICES, default=1)
    category = models.ManyToManyField("Category")
    clinic = models.ManyToManyField(Clinic)

    def __str__(self) -> str:
        return self.first_name + self.last_name


# Many to Many relation
class Category(models.Model):
    """Category object."""

    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(
        max_length=255, unique=True, validators=[validate_name]
    )

    def __str__(self) -> str:
        return self.category_name
