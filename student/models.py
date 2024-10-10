from django.db import models
from address.models import College, District


class AcademicYear(models.Model):
    year = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.year}"


class HomeTown(models.Model):
    district = models.CharField(max_length=20)


class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    name = models.CharField(max_length=30)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    roll = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    gurdian_phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    home_town = models.ForeignKey(
        District, on_delete=models.CASCADE, null=True, blank=True)
    college = models.ForeignKey(
        College, on_delete=models.CASCADE, null=True, blank=True)
    year = models.ForeignKey(AcademicYear, null=True,
                             blank=True, on_delete=models.CASCADE)
    address = models.TextField(max_length=255, blank=True, null=True)
    remark = models.TextField(max_length=255, blank=True, null=True)
    crated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
