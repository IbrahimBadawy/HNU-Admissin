# Generated by Django 5.2 on 2025-04-30 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="profile_img",
            field=models.ImageField(
                blank=True, default="images/default.png", null=True, upload_to="images"
            ),
        ),
    ]
