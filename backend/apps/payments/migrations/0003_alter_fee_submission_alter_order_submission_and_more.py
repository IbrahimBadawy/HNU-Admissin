# Generated by Django 5.2 on 2025-05-07 12:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admissions', '0020_alter_formsubmission_form'),
        ('payments', '0002_remove_fee_submission_id_remove_order_submission_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fee',
            name='submission',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fees', to='admissions.formsubmission'),
        ),
        migrations.AlterField(
            model_name='order',
            name='submission',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='admissions.formsubmission'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='order',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='payments.order'),
        ),
    ]
