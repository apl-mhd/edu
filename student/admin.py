from django.contrib import admin
from .models import Student, AcademicYear, Day, Batch

# Register your models here.

admin.site.register([Student, AcademicYear, Day, Batch])
