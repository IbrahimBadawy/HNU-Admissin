# Generated by Django 5.2 on 2025-05-03 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("admissions", "0006_remove_question_option"),
    ]

    operations = [
        migrations.RenameField(
            model_name="question",
            old_name="config",
            new_name="configs",
        ),
    ]
