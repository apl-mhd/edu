from django.urls import path, include
from .views import PaymentView, CourseAssingView
urlpatterns = [
    path('payment/', PaymentView.as_view(), name='payment'),
    path('course-assign/', CourseAssingView.as_view(), name='course-assign'),
]
