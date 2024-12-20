from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('student/', include('student.urls')),
    path('course/', include('course.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('user/', include('users.urls')),

]
