from django.urls import path
from .views import IndexTemplateView, ExampleView, CustomAuthToken


urlpatterns = [
    path('', IndexTemplateView.as_view(), name='dashboard'),
    path('authentication/', CustomAuthToken.as_view(), name='authentication')
]
