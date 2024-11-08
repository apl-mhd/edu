from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [

    # path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    # path('login/', views.LoginTamplateView.as_view(template_name='users/login.html'), name='login'),
    path('login/', views.LoginView.as_view(), name='user-login'),
    # path('test/', views.test, name='user-test'),

]
