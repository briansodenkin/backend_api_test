from django.db import migrations, models, transaction


# Bulk create the Districts
def create_default_district(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    District = apps.get_model("district", "District")
    districts = [
        "Central and Western",
        "Eastern",
        "Southern",
        "Wan Chai",
        "Kowloon City",
        "Kwun Tong",
        "Sham Shui Po",
        "Wong Tai Sin",
        "Yau Tsim Mong",
    ]

    with transaction.atomic():
        bulk_list = list()
        for district in districts:
            bulk_list.append(District(district_name=district))
        District.objects.bulk_create(bulk_list)


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="District",
            fields=[
                ("district_id", models.AutoField(primary_key=True, serialize=False)),
                ("district_name", models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.RunPython(create_default_district),
    ]
