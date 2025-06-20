# Generated by Django 5.2 on 2025-06-21 02:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0003_programfee"),
        ("users", "0006_academicyear"),
    ]

    operations = [
        migrations.AlterField(
            model_name="programfee",
            name="academic_year",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="fees_by_year",
                to="users.academicyear",
            ),
        ),
        migrations.AlterField(
            model_name="programfee",
            name="fee_list",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="fees_by_list",
                to="payments.feeslist",
            ),
        ),
        migrations.AlterField(
            model_name="programfee",
            name="program",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="fees_by_program",
                to="users.program",
            ),
        ),
    ]
