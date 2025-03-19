from django.contrib import admin
from django.urls import path, include
from address import apiviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/students/', include('student.urls')),
    path('api/districts/', include('address.urls')),
    path('api/courses/', include('course.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('user/', include('users.urls')),
]
