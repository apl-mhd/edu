from django.urls import path, include
from .views import PaymentView
urlpatterns = [
    path('payment/', PaymentView.as_view(), name='payment'),
]
