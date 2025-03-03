# Generated by Django 5.1.6 on 2025-03-03 13:36

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("candidates", "0004_auto_20250303_1336"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="candidate",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["name"], name="candidates__name_1a7d0c_gin"
            ),
        ),
    ]
