# Generated by Django 5.1.1 on 2024-10-17 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0009_alter_payment_payment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentbilling',
            name='course_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='studentbilling',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]