# Generated by Django 5.1.1 on 2024-11-01 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0009_alter_student_batch'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='student',
            name='student_roll',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]
