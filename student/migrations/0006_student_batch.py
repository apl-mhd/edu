# Generated by Django 5.1.1 on 2024-10-20 10:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_day_batch'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='batch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.batch'),
        ),
    ]