from django.shortcuts import render
from django.http import HttpResponse
from pathlib import Path
import os
from address.models import District, College
from course.models import Course
from .models import AcademicYear, Student
from course.models import StudentEnroll, Payment
import json
from .serializers import StudentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
# Create your views here.


class StudentList(APIView):
    def get(self, requst, *args, **kwargs):
        students = Student.objects.all()
        a = Student.objects.values(
            "id", "name", "hsc_batch__year", "gender").all()

        payment = Student.objects.prefetch_related('payments').values()
        print(payment[0])

        # for i in payment:
        #     for j in i.payments.all():
        #         print(j)

        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


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

    return HttpResponse("apel")


def index(request):
    district = District.objects.all()
    print(district)
    return render(request, 'index.html')


def student(request):
    district_list = District.objects.all().values("id", "name")
    college_list = College.objects.all().values("id", "name")
    course_list = Course.objects.all().values("id", "name")
    academic_year_list = AcademicYear.objects.all().order_by(
        '-hsc_batch').values('id', 'hsc_batch')

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

    return render(request, 'student.html', context=context)
