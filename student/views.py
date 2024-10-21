from django.shortcuts import render
from django.http import HttpResponse
from pathlib import Path
import os
from address.models import District, College
from course.models import Course, Payment, Discount, StudentEnroll
from .models import AcademicYear, Student, Batch
from course.models import StudentBilling
import json
from .serializers import StudentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
# Create your views here.
from django.db.models import Subquery, Sum, OuterRef, When, Case, Exists, Value, F
from django.utils import timezone

from django.db.models.functions import Coalesce


# class StudentFilter(APIView):


class StudentList(APIView):
    def get(self, requst, *args, **kwargs):

        current_month = timezone.now().replace(
            day=1)

        current_month_payment_exists = Payment.objects.filter(
            student=OuterRef('pk'),
            payment_date__month=current_month.month,
            payment_date__year=current_month.year
        ).values('id')

        students = Student.objects.annotate(
            total_course_amount=Subquery(
                StudentEnroll.objects.filter(student=OuterRef('pk')).values('student').annotate(
                    total=Sum('course_fee')
                ).values('total')
            ),
            total_discount=Subquery(
                Discount.objects.filter(student=OuterRef('pk')).values('student').annotate(
                    total=Sum('discount_amount')
                ).values('total')
            ),

            total_payment=Subquery(
                Payment.objects.filter(student=OuterRef('pk')).values('student').annotate(
                    total=Sum('amount_payment')
                ).values('total')
            ),
            due_amount=Coalesce(F('total_course_amount'), Value(0)) -
            Coalesce(F('total_discount'), Value(0)) -
            Coalesce(F('total_payment'), Value(0)),

            paid_current_month=Case(
                When(Exists(current_month_payment_exists), then=Value(True)),
                default=Value(False)
            ),

        ).values('id', 'name', 'hsc_batch__year', 'total_course_amount', 'total_discount', 'total_payment', 'paid_current_month', 'due_amount').order_by('-id')

        data = students
        return Response(data)


class StudentListTest(APIView):
    def get(self, requst, *args, **kwargs):

        current_month = timezone.now().replace(
            day=1)

        current_month_payment_exists = Payment.objects.filter(
            student=OuterRef('pk'),
            payment_date__month=current_month.month,
            payment_date__year=current_month.year
        ).values('id')

        students = Student.objects.annotate(
            total_course_amount=Subquery(
                StudentBilling.objects.filter(student=OuterRef('pk')).values('student').annotate(
                    total=Sum('course_fee')
                ).values('total')
            ),
            total_discount=Subquery(
                StudentBilling.objects.filter(student=OuterRef('pk')).values('student').annotate(
                    total=Sum('discount')
                ).values('total')
            ),
            total_payment=Subquery(
                Payment.objects.filter(student=OuterRef('pk')).values('student').annotate(
                    total=Sum('amount_payment')
                ).values('total')
            ),
            due_amount=F('total_course_amount') -
            Coalesce(F('total_discount'), Value(0)) -
            Coalesce(F('total_payment'), Value(0)),

            paid_current_month=Case(
                When(Exists(current_month_payment_exists), then=Value(True)),
                default=Value(False)
            ),

        ).values('id', 'name', 'hsc_batch__year', 'total_course_amount', 'total_discount', 'total_payment', 'paid_current_month', 'due_amount').order_by('-id')

        # students = Student.objects.all()

        # serializer = StudentSerializer(students, many=True)
        data = students
        return Response(data)


class StudentCreateView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            serializer_data = StudentSerializer(data=request.data)
            if serializer_data.is_valid():
                serializer_data.save()
                return Response(serializer_data.data)
            else:
                print("else")
                print(serializer_data.errors)
                return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'status': 'failed', 'message': 'something went wrong'})


# Not needed
def index(request):
    district = District.objects.all()
    print(district)
    return render(request, 'index.html')


def student(request):
    district_list = District.objects.all().values("id", "name")
    college_list = College.objects.all().values("id", "name")
    course_list = Course.objects.all().values("id", "name", "course_fee")
    academic_year_list = AcademicYear.objects.all().values('id', 'year')
    batches = Batch.objects.all()

    batch_list = [{"id": i.id, "title": i.get_batch_details()}
                  for i in batches]

    context = {
        'home_town_list': json.dumps(list(district_list)),
        'college_list': json.dumps(list(college_list)),
        'course_list': json.dumps(list(course_list)),
        'academic_year_list': json.dumps(list(academic_year_list)),
        'batch_list': json.dumps(list(batch_list)),
    }

    return render(request, 'student.html', context=context)
