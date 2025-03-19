from django.urls import path
from . import views, apiviews

urlpatterns = [
    path("", views.StudentTemplateView.as_view(), name='students'),
    path("<int:pk>/", views.StudentDetailView.as_view(),
         name='students-detail'),
    path("create/", apiviews.StudentCreateView.as_view(), name='students-create'),
    path("update/<int:pk>/", views.StudentDetailView.as_view(),
         name='students-update'),
    path("all/", views.StudentList.as_view(), name='student-all'),
    path("filter/", views.StudentListFilter.as_view(), name='student-filter'),
    path("report/", views.studentReportListView.as_view(), name='report'),
]
