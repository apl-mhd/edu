from django.urls import path
from . import apiviews
urlpatterns = [
    path('', apiviews.CourseAPIView.as_view(), name='courses'),
    path('payment/', apiviews.PaymentView.as_view(), name='payment'),
    path('course-assign/', apiviews.CourseAssingView.as_view(), name='course-assign'),
    path('student-payment-list/<int:id>/', apiviews.StudentPaymentListView.as_view(),
         name='student-payment-list'),
]
