from django.db import models


# Create your models here.
class District(models.Model):
    """District object."""

    district_id = models.AutoField(primary_key=True)
    district_name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.district_name
