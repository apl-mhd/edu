from django.contrib import admin
from .models import Student, AcademicYear

# Register your models here.

admin.site.register(Student)
admin.site.register(AcademicYear)
