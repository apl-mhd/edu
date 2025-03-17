from django.contrib import admin
from django.urls import path, include
from address import apiviews

urlpatterns = [
    path('api/students/', include('student.urls')),
    path('api/districts/', include('address.urls')),
    path('admin/', admin.site.urls),
    path('students/', include('student.urls')),
    path('student/', include('student.urls')),
    path('course/', include('course.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('user/', include('users.urls')),
]
