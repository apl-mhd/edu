# Generated by Django 5.1.1 on 2024-10-18 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0022_alter_payment_amount_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentbilling',
            name='fee_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
