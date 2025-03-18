from django.urls import path, include
from .views import PaymentView, CourseAssingView, StudentPaymentListView
from . import apiviews
urlpatterns = [
    path('', apiviews.CourseAPIView.as_view(), name='courses'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('course-assign/', CourseAssingView.as_view(), name='course-assign'),
    path('student-payment-list/<int:id>/', StudentPaymentListView.as_view(),
         name='student-payment-list'),
]