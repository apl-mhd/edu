# Generated by Django 5.1.1 on 2024-10-18 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0019_alter_batch_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='days',
            field=models.ManyToManyField(related_name='days', to='course.day'),
        ),
    ]
