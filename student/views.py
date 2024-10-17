from django.shortcuts import render
from django.http import HttpResponse
from pathlib import Path
import os
from address.models import District, College
from course.models import Course, Payment
from .models import AcademicYear, Student
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
                StudentBilling.objects.filter(student=OuterRef('pk')).values('student').annotate(
                    total=Sum('course_amount')
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
            F('total_discount') - F('total_payment'),

            paid_current_month=Case(
                When(Exists(current_month_payment_exists), then=Value('Yes')),
                default=Value('No')
            )
        ).values('id', 'name', 'hsc_batch__year', 'total_course_amount', 'total_discount', 'total_payment', 'paid_current_month', 'due_amount').order_by('-id')

        # students = Student.objects.all()

        # serializer = StudentSerializer(students, many=True)
        data = students
        return Response(data)


class StudentView(APIView):

    def post(self, request, *args, **kwargs):

        try:
            print(request.data.get("phone"))
            serializer_data = StudentSerializer(data=request.data)
            if serializer_data.is_valid():
                serializer_data.save()
                print(serializer_data.validated_data)
                return Response(serializer_data.data)
            else:
                print("else")
                print(serializer_data.errors)
                return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'status': 'failed', 'message': 'something went wrong'})


@api_view(['POST'])
def studentCreate(request):

    a = {"name": "apel", "x": "y"}
    serializer_data = StudentSerializer(data=a)
    if serializer_data.is_valid():
        print("if")
        print(serializer_data.validated_data)
        return Response(serializer_data.data)
    else:
        print("else")
        print(serializer_data.errors)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)


def index(request):
    district = District.objects.all()
    print(district)
    return render(request, 'index.html')


def student(request):
    district_list = District.objects.all().values("id", "name")
    college_list = College.objects.all().values("id", "name")
    course_list = Course.objects.all().values("id", "name")
    academic_year_list = AcademicYear.objects.all().order_by(
        '-id').values('id', 'year')

    # {'name': 'adf', 'phone': 'ad', 'gurdian_phone': 'ad', 'email': 'admin@mail.com', 'gender': 'M', 'course': 1, 'hsc_batch': 2, 'home_town': 1, 'college': 1}
    if request.method == 'POST':
        data = json.loads(request.body)
        if data['course']:
            data['course'] = Course.objects.filter(id=data['course']).first()

        else:
            data['course'] = None

        if data['hsc_batch']:
            data['hsc_batch'] = AcademicYear.objects.filter(
                id=data['hsc_batch']).first()

        else:
            data['hsc_batch'] = None

        if data['home_town']:
            data['home_town'] = District.objects.filter(
                id=data['home_town']).first()
        else:
            data['home_town'] = None

        if data['college']:
            data['college'] = College.objects.filter(
                id=data['college']).first()

        else:
            data['college'] = None

        data.pop('course')

        a = {"name": "apel", "x": "y"}

        serializer_data = StudentSerializer(data=a)
        if serializer_data.is_valid():
            print("ifaa")
            print(serializer_data.validated_data)
        else:
            print("else")
            print(serializer_data.errors)
            return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

        return HttpResponse("apel")

    context = {
        'home_town_list': json.dumps(list(district_list)),
        'college_list': json.dumps(list(college_list)),
        'course_list': json.dumps(list(course_list)),
        'academic_year_list': json.dumps(list(academic_year_list)),
    }

    print(list(academic_year_list))

    return render(request, 'student.html', context=context)
