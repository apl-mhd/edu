from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("create/", views.student, name='student-create'),
    path("test/", views.StudentView.as_view(), name='student-test'),
    path("all/", views.StudentList.as_view(), name='student-test')
]
