from django.conf import settings
from django.db import models
from student.models import Student
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator

# # Create your models here.


class Day(models.Model):
    DAYS_CHOICES = (
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    )

    name = models.CharField(max_length=20, choices=DAYS_CHOICES, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    price = models.IntegerField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Batch(models.Model):
    name = models.CharField(max_length=50)
    days = models.ManyToManyField(Day, related_name='days')
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - From {self.start_time} To {self.end_time}"


class StudentEnroll(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, null=True, blank=True)
    batch = models.ForeignKey(
        Batch, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # created_by = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return self.course.name


class StudentBilling(models.Model):

    FEE_TYPES = [
        ('tuition', 'Tuition Fee'),
        ('course', 'course Fee'),
        ('discount', 'Discount'),
        ('exam', 'Exam Fee'),
        ('material', 'Material Fee'),
        ('other', 'Other'),
    ]

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='billing')
    fee_type = models.CharField(
        max_length=100, choices=FEE_TYPES, null=True, blank=True)
    course = models.ForeignKey(
        Course, null=True, blank=True, on_delete=models.CASCADE)
    course_amount = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    remark = models.TextField(null=True, blank=True)
    # created_by = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return f"{self.student.name}-{self.course.name}-{self.course_amount}"


class Payment(models.Model):
    PAYMENT_TYPES = [
        ('tuition', 'Tuition Fee'),
        ('exam', 'Exam Fee'),
        ('material', 'Material Fee'),
        ('other', 'Other'),
    ]

    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('mobile', 'Mobile Payment'),
        ('bank', 'Bank Transfer'),
    ]

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='payments')
    amount_payment = models.IntegerField(validators=[MinValueValidator(1)])
    payment_date = models.DateTimeField(default=timezone.now)
    payment_type = models.CharField(
        max_length=20, choices=PAYMENT_TYPES, null=True, blank=True, default='tuition')
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHODS, null=True, blank=True)
    status = models.CharField(max_length=20, default='completed')
    reference_number = models.CharField(max_length=250, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.student} - {self.amount_payment} on {self.payment_date}"
