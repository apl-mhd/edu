# Generated by Django 5.1.1 on 2024-10-20 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0024_alter_studentbilling_fee_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ['-id']},
        ),
        migrations.RemoveField(
            model_name='studentenroll',
            name='batch',
        ),
    ]