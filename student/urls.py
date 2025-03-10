from django.urls import path
from . import views, apiviews

urlpatterns = [
    # path("", views.index, name='index'),
    path("data-form/", apiviews.StudentDataFormAPIView.as_view(),
         name='student-data-form'),
    path("<int:pk>/", views.StudentDetailView.as_view(), name='student-detail'),
    path("create/", views.StudentTemplateView.as_view(), name='student-create'),
    path("test/", views.StudentCreateView.as_view(), name='student-test'),
    path("all/", views.StudentList.as_view(), name='student-all'),
    path("filter/", views.StudentListFilter.as_view(), name='student-filter'),
    path("list-test/", views.StudentListTest.as_view(), name='student-list-test'),
    path("report/", views.studentReportListView.as_view(), name='report'),
]
