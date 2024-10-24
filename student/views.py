from django.shortcuts import render
from django.http import HttpResponse
from pathlib import Path
import os
from address.models import District, College
from course.models import Course, Payment, Discount, StudentEnroll
from course.serializers import PaymentSerializer
from .models import AcademicYear, Student, Batch
from course.models import StudentBilling
import json
from .serializers import StudentSerializer
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


# class StudentFilter(APIView):

class StudentListFilter(ListAPIView):
    # serializer_class = PaymentSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):

        q_name = self.request.query_params.get('name', None)
        q_year = self.request.query_params.get('year', None)
        q_batch = self.request.query_params.get('batch', None)
        q = self.request.query_params.get('q', None)

        current_month = timezone.now().replace(
            day=1)

        current_month_payment_exists = Payment.objects.filter(
            student=OuterRef('pk'),
            payment_date__month=current_month.month,
            payment_date__year=current_month.year
        ).values('id')

        students = Student.objects

        if q and q.isdigit():
            students = students.filter(
                Q(hsc_batch__year=q))
        elif q:
            students = students.filter(
                Q(name__icontains=q) | Q(batch__name__icontains=q))


        students = students.select_related('batch').select_related('hsc_batch').annotate(
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
                    total=Sum('payment_amount')
                ).values('total')
            ),
            due_amount=Coalesce(F('total_course_amount'), Value(0)) -
            Coalesce(F('total_discount'), Value(0)) -
            Coalesce(F('total_payment'), Value(0)),

            paid_current_month=Case(
                When(Exists(current_month_payment_exists), then=Value(True)),
                default=Value(False)
            )).values('id', 'name', 'hsc_batch__year', 'total_course_amount', 'total_discount', 'total_payment', 'paid_current_month', 'due_amount', 'batch__name', 'batch__start_time', 'batch__end_time')
        
        filter_by = self.request.query_params.get('filter_by', None)

        print(self.request.query_params.get)
    
        if filter_by and filter_by is not '-':
            students = students.order_by(filter_by)
        
        
        

        # data = {"name": "Sort by name",
        #         "batch__name": "Sort by batch", "hsc_batch__year": "Sort by HSC", "due_amount": "Sort by due amount", "paid_current_month": "Sort by current month"}

        return students

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(page)

        data = queryset
        return Response(data)

    # def list(self):
    #     queryset = super().get_queryset()
    #     data = list(queryset.values())
    #     return Response(data)

    # def get(self, request):
    #     payment = Payment.objects.all()
    #     results = self.paginate_queryset(payment, request, view=self)
    #     serializer = PaymentSerializer(results, many=True)
    #     return self.get_paginated_response(serializer.data)

    # def get(self, request):
    #     payment = Payment.objects.all()
    #     data = PaymentSerializer(payment, many=True)
    #     return Response(data.data)


class StudentList(APIView):
    def get(self, requst, *args, **kwargs):

        current_month = timezone.now().replace(
            day=1)

        current_month_payment_exists = Payment.objects.filter(
            student=OuterRef('pk'),
            payment_date__month=current_month.month,
            payment_date__year=current_month.year
        ).values('id')

        students = Student.objects.select_related('batch').annotate(
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
                    total=Sum('payment_amount')
                ).values('total')
            ),
            due_amount=Coalesce(F('total_course_amount'), Value(0)) -
            Coalesce(F('total_discount'), Value(0)) -
            Coalesce(F('total_payment'), Value(0)),

            paid_current_month=Case(
                When(Exists(current_month_payment_exists), then=Value(True)),
                default=Value(False)
            )).values('id', 'name', 'hsc_batch__year', 'total_course_amount', 'total_discount', 'total_payment', 'paid_current_month', 'due_amount', 'batch__name', 'batch__start_time', 'batch__end_time').order_by('-id')

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

        students = Student.objects.select_related('batch').annotate(
            total_course_amount=Subquery(
                StudentBilling.objects.filter(student=OuterRef('pk')).values('student').annotate(
                    total=Sum('course_fee')
                ).values('total')
            ),
            total_payment=Subquery(
                Payment.objects.filter(student=OuterRef('pk')).values('student').annotate(
                    total=Sum('payment_amount')
                ).values('total')
            ),
            due_amount=F('total_course_amount') -
            Coalesce(F('total_payment'), Value(0)),

            paid_current_month=Case(
                When(Exists(current_month_payment_exists), then=Value(True)),
                default=Value(False)
            ),

            batch_details=Concat(
                'batch__name',
                Value(' - '),
                Cast('batch__start_time', output_field=CharField()),
                Value(' to '),
                Cast('batch__end_time', output_field=CharField()),
                output_field=CharField()
            )

        ).values('id', 'name', 'hsc_batch__year', 'total_course_amount', 'total_payment', 'paid_current_month', 'due_amount', 'batch_details').order_by('-id')

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
                return Response(data={"message": "Successfully student created.", "data": serializer_data.data}, status=status.HTTP_201_CREATED)
            else:
                for i in serializer_data.errors:
                    print(i)
                return Response(data={"message": "Fill correctly all the required Field", "errors": serializer_data.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'status': 'failed', 'message': 'something went wrong'})


# Not needed
def index(request):
    district = District.objects.all()
    print(district)
    return render(request, 'index.html')


class StudentTemplateView(TemplateView):
    template_name = 'student.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        district_list = District.objects.all().values("id", "name")
        college_list = College.objects.all().values("id", "name")
        course_list = Course.objects.all().values("id", "name", "course_fee")
        academic_year_list = AcademicYear.objects.all().values('id', 'year')
        batches = Batch.objects.all()

        batch_list = [{"id": i.id, "title": i.get_batch_details()}
                      for i in batches]

        context['home_town_list'] = json.dumps(list(district_list))
        context['college_list'] = json.dumps(list(college_list))
        context['course_list'] = json.dumps(list(course_list))
        context['academic_year_list'] = json.dumps(list(academic_year_list))
        context['batch_list'] = json.dumps(list(batch_list))

        return context


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
