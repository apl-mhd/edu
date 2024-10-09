from django.db import models
from student.models import Student
from django.contrib.auth.models import User


# #
# # Create your models here.


class Day(models.Model):
    name = models.CharField(max_length=20)
    crated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    crated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Batch(models.Model):

    DAYS_CHOICES = (
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    )

    name = models.CharField(max_length=50)
    days = models.ManyToManyField(Day)
    start_time = models.TimeField()
    end_time = models.TimeField()
    crated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class StudentEnroll(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    crated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # created_by = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return self.course


class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_type = models.CharField(max_length=100)
    course = models.ForeignKey(
        Course, null=True, blank=True, on_delete=models.CASCADE)
    course_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    payment = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)

    crated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    remark = models.TextField(null=True, blank=True)
    # created_by = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return self.fee_type
