# Generated by Django 5.2 on 2025-06-21 12:05

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0008_alter_fee_fee_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="fee",
            name="created_at",
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="fee",
            name="modified_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
