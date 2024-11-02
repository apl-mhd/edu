from django.db import models
from address.models import College, District
from django.core.validators import MaxValueValidator, MinValueValidator


class Day(models.Model):
    DAYS_CHOICES = (
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
    )

    name = models.CharField(max_length=20, choices=DAYS_CHOICES, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.name}"


class Batch(models.Model):
    name = models.CharField(max_length=50)
    days = models.ManyToManyField(Day, related_name='days')
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_batch_details()

    def get_batch_details(self):
        day_names = ""
        for day in self.days.all():
            day_names += f"-{day.name}"

        return f"{self.name} {day_names}- From {self.start_time.strftime('%I:%M %p')} To {self.end_time.strftime('%I:%M %p')}"


class AcademicYear(models.Model):
    year = models.IntegerField(
        unique=True,
        validators=[MinValueValidator(2010), MaxValueValidator(2050)])
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return f"{self.year}"


class HomeTown(models.Model):
    district = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.district


class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    student_roll = models.IntegerField(unique=True)
    name = models.CharField(max_length=30)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    phone = models.CharField(max_length=20, unique=True)
    gurdian_phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    home_town = models.ForeignKey(
        District, on_delete=models.CASCADE, null=True, blank=True)
    college = models.ForeignKey(
        College, on_delete=models.CASCADE, null=True, blank=True)
    ssc_batch = models.ForeignKey(AcademicYear, null=True,
                                  blank=True, on_delete=models.CASCADE, related_name='ssc_batch')
    hsc_batch = models.ForeignKey(
        AcademicYear, on_delete=models.CASCADE, related_name='hsc_batch')
    ssc_gpa = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True)
    hsc_gpa = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True)
    batch = models.ForeignKey(
        Batch, on_delete=models.CASCADE, related_name="batch_name")
    address = models.TextField(max_length=255, blank=True, null=True)
    remark = models.TextField(max_length=255, blank=True, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name
