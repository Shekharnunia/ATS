# Generated by Django 5.1.6 on 2025-03-03 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("candidates", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="candidate",
            name="gender",
            field=models.CharField(
                choices=[("MALE", "Male"), ("FEMALE", "Female"), ("OTHER", "Other")],
                max_length=6,
            ),
        ),
    ]
