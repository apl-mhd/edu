# Generated by Django 5.1.1 on 2024-10-17 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0010_alter_studentbilling_course_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='course',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
