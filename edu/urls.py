from django.contrib import admin
from django.urls import path, include
from address import apiviews
from student.views import StudentTemplateView

urlpatterns = [
    path("", StudentTemplateView.as_view(), name='students'),
    path('api/students/', include('student.urls')),
    path('api/districts/', include('address.urls')),
    path('admin/', admin.site.urls),
    path('students/', include('student.urls')),
    path('student/', include('student.urls')),
    path('api/courses/', include('course.urls')),
    path('course/', include('course.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('user/', include('users.urls')),
]
