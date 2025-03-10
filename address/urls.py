from .models import District
from .apiviews import DistrictListAPIView, test, DistrictCreateView, DistrictUpdateView, DistrictDeleteView
from django.urls import path

urlpatterns = [
    path('', DistrictListAPIView.as_view(), name='district-list'),
    path('create/', DistrictCreateView.as_view(), name='district-create'),
    path('update/<int:pk>/', DistrictUpdateView.as_view(), name='district-update'),
    path('delete/<int:pk>/', DistrictDeleteView.as_view(), name='district-delete'),
    path('test/', test, name='district-test'),
]
