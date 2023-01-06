import random

import django.db.models.deletion
from django.db import migrations, models, transaction
from faker import Faker


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10**n) - 1
    return random.randint(range_start, range_end)


# Bulk create clinic
def create_default_clinic_phone(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    fake = Faker()
    name_address_list = [(fake.name(), fake.address()) for _ in range(10)]
    Clinic = apps.get_model("clinic", "Clinic")
    District = apps.get_model("district", "District")
    Phone = apps.get_model("clinic", "Phone")
    with transaction.atomic():
        bulk_list = list()
        for name, address in name_address_list:
            district_id = random.randint(1, 9)
            district = District.objects.filter(district_id=district_id).first()
            bulk_list.append(
                Clinic(clinic_name=name, clinic_address=address, district=district)
            )
        Clinic.objects.bulk_create(bulk_list)
        for i in range(1, 11):
            clinic = Clinic.objects.filter(clinic_id=i).first()
            Phone.objects.create(phone_number=random_with_N_digits(8), clinic=clinic)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("district", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Clinic",
            fields=[
                ("clinic_id", models.AutoField(primary_key=True, serialize=False)),
                ("clinic_name", models.CharField(max_length=255)),
                ("clinic_address", models.CharField(max_length=255, unique=True)),
                (
                    "district",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="district",
                        to="district.district",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Phone",
            fields=[
                ("phone_id", models.AutoField(primary_key=True, serialize=False)),
                ("phone_number", models.SmallIntegerField()),
                (
                    "clinic",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="clinic",
                        to="clinic.clinic",
                    ),
                ),
            ],
        ),
        migrations.RunPython(create_default_clinic_phone),
    ]
