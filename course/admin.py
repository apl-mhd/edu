from django.contrib import admin
from . models import *

# Register your models here.

admin.site.register(Day)
admin.site.register(Course)
admin.site.register(Batch)
admin.site.register(StudentEnroll)
admin.site.register(StudentBilling)
