# Generated by Django 4.0.5 on 2023-01-05 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("district", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="district",
            name="district_name",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]