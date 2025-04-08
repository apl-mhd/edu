from django.urls import path
from . import views, apiviews, testviews
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path("create/", apiviews.StudentCreateView.as_view(), name='students-create'),
    path("data-form/", apiviews.StudentDataFormAPIView.as_view(),
         name='student-data-form'),
    path("<int:pk>/", apiviews.StudentDetailView.as_view(), name='student-detail'),
    path("update/<int:pk>/", apiviews.StudentDetailView.as_view(),
         name='students-update'),
    path("filter/", apiviews.StudentListFilter.as_view(), name='student-filter'),
    path("report/", views.studentReportListView.as_view(), name='report'),


    path("test/", testviews.ExampleView.as_view()),
    path('token/', TokenObtainPairView.as_view())


]
