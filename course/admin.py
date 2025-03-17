from django.contrib import admin
from . models import *

# Register your models here.

admin.site.register(Course)
admin.site.register(StudentEnroll)
admin.site.register(Fee)
admin.site.register(Payment)
