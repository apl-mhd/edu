# Generated by Django 5.1.1 on 2024-11-01 11:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0010_alter_student_options_student_student_roll'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='hsc_batch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='hsc_batch', to='student.academicyear'),
            preserve_default=False,
        ),
    ]
