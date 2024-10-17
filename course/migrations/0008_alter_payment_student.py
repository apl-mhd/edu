# Generated by Django 5.1.1 on 2024-10-16 16:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_alter_payment_student_alter_studentbilling_student'),
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='student.student'),
        ),
    ]