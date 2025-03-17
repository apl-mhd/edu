from django.shortcuts import render
from django.http import HttpResponse
from pathlib import Path
import os
from address.models import District, College
from course.models import Course, Payment, Discount, StudentEnroll
from course.serializers import PaymentSerializer
from student.models import AcademicYear, Student, Batch
from course.models import Fee
import json
from student.serializers import StudentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.views.generic.base import TemplateView
# Create your views here.
from django.db.models import Subquery, Sum, OuterRef, When, Case, Exists, Value, F, CharField, Q
from django.utils import timezone

from django.db.models.functions import Coalesce, Concat, Cast
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class ExampleView(APIView):
    user = User.objects.first()
    # token = Token.objects.create(user=user)

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # parser_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }

        return Response(content)


class IndexTemplateView(TemplateView):

    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        start_of_month = timezone.now().replace(day=1,
                                                hour=0, minute=0, second=0, microsecond=0)

        today_of_month = timezone.now().replace(
            hour=0, minute=0, second=0, microsecond=0)

        total_amount = Payment.objects.aggregate(
            total=Sum('payment_amount'))

        total_student = Student.objects.aggregate(
            total=Sum(1)
        )

        todays_payment = Payment.objects.filter(Q(payment_date__gte=today_of_month), Q(payment_date__lte=timezone.now())
                                                ).aggregate(total_amount=Sum('payment_amount'), total_student=Sum(1))

        monthly_payment = Payment.objects.filter(
            payment_date__gte=start_of_month).aggregate(total_amount=Sum('payment_amount'), total_student=Sum(1))

        data = {
            "total_payment_amount": total_amount['total'],
            "total_student": total_student['total'],
            "today": {"total_payment_amount": todays_payment['total_amount'], "total_student": todays_payment["total_student"]},
            "month": {"total_payment_amount": monthly_payment['total_amount'], "total_student": monthly_payment["total_student"]},
        }

        context['data'] = json.dumps(data)
        # context['college_list'] = json.dumps(list(college_list))
        # context['course_list'] = json.dumps(list(course_list))
        # context['academic_year_list'] = json.dumps(list(academic_year_list))
        # context['batch_list'] = json.dumps(list(batch_list))
        return context
