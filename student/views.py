from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from pathlib import Path
import os
from address.models import District, College
from course.models import Course
from .models import AcademicYear, Student
import json


# Create your views here.


def index(request):
    district = District.objects.all()
    print(district)
    return render(request, 'index.html')


def student(request):
    district_list = District.objects.all().values("id", "name")
    college_list = College.objects.all().values("id", "name")
    course_list = Course.objects.all().values("id", "name")
    academic_year_list = AcademicYear.objects.all().order_by(
        '-year').values('id', 'year')

# {'name': 'adf', 'phone': 'ad', 'gurdian_phone': 'ad', 'email': 'admin@mail.com', 'gender': 'M', 'course': 1, 'year': 2, 'home_town': 1, 'college': 1}
    if request.method == 'POST':
        data = json.loads(request.body)
        if data['course']:
            data['course'] = Course.objects.filter(id=data['course']).first()

        else:
            data['course'] = None

        if data['year']:
            data['year'] = AcademicYear.objects.filter(
                id=data['year']).first()

        else:
            data['year'] = None

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

        print(data)
        data.pop('course')
        Student.objects.create(**data)
        return HttpResponse("apel")

    context = {
        'home_town_list': json.dumps(list(district_list)),
        'college_list': json.dumps(list(college_list)),
        'course_list': json.dumps(list(course_list)),
        'academic_year_list': json.dumps(list(academic_year_list)),
    }

    return render(request, 'student.html', context=context)
