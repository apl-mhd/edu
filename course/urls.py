from django.urls import path, include
from .views import PaymentView, CourseAssingView, StudentPaymentListView
urlpatterns = [
    path('payment/', PaymentView.as_view(), name='payment'),
    path('course-assign/', CourseAssingView.as_view(), name='course-assign'),
    path('student-payment-list/<int:id>/', StudentPaymentListView.as_view(),
         name='student-payment-list'),
]
