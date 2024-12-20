# Generated by Django 5.1.1 on 2024-10-21 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0031_rename_amount_payment_payment_payment_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentbilling',
            name='discount',
        ),
        migrations.AlterField(
            model_name='studentbilling',
            name='fee_type',
            field=models.CharField(blank=True, choices=[('tuition', 'Tuition Fee'), ('course', 'course Fee'), ('exam', 'Exam Fee'), ('material', 'Material Fee'), ('other', 'Other')], max_length=100, null=True),
        ),
    ]
