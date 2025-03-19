from django.db.models.functions import *
from django.db.models import Count, Avg, Case, When, IntegerField
from django.utils.timezone import now, timedelta
from django.shortcuts import render
from address.models import District, College
from course.models import Course, Payment, Discount, StudentEnroll
from course.serializers import PaymentSerializer
from .models import AcademicYear, Student, Batch
from course.models import Fee
import json
from .serializers import StudentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from django.views.generic.base import TemplateView
# Create your views here.
from django.db.models import Subquery, Sum, OuterRef, When, Case, Exists, Value, F, CharField, Q, Max
from django.utils import timezone

from django.db.models.functions import Coalesce, Concat, Cast
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django_xhtml2pdf.utils import generate_pdf
from django.views.generic.list import ListView
from django_xhtml2pdf.views import PdfMixin
from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomPagination(PageNumberPagination):
    page_size = 1  # Number of records per page
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            "count": self.page.paginator.count,
            "total_pages": self.page.paginator.num_pages,
            "current_page": self.page.number,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data  # Rename "results" to "data"
        })


class StudentDetailView(RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class studentReportListView(LoginRequiredMixin, PdfMixin, ListView):
    template_name = 'report.html'

    def get_queryset(self):

        self.batch = self.request.GET.get('batch', None)
        if self.batch == '':
            return {}

        if self.batch:
            self.batch = Batch.objects.filter(pk=self.batch).first()
            if not self.batch:
                return {}

        current_month = timezone.now().replace(
            day=1)

        current_month_payment_exists = Payment.objects.filter(
            student=OuterRef('pk'),
            payment_date__month=current_month.month,
            payment_date__year=current_month.year,
        ).values('id')

        students = Student.objects

        students = students.prefetch_related('payments').filter(batch=self.batch).annotate(
            total_payment=Subquery(
                Payment.objects.filter(student=OuterRef('pk')).values('student').annotate(
                    total=Sum('payment_amount')).values('total')
            ),

            total_discount=Subquery(
                Discount.objects.filter(student=OuterRef('pk')).values('student').annotate(
                    total=Sum('discount_amount')).values('total')
            ),

            total_course_amount=Subquery(
                StudentEnroll.objects.filter(student=OuterRef('pk')).values('student').annotate(
                    total=Sum('course_fee')).values('total')
            ),

            due_amount=Coalesce(F('total_course_amount'), Value(
                0)) - Coalesce(F('total_discount'), Value(0)) - Coalesce(F('total_payment'), Value(0)),

            paid_current_month=Case(
                When(Exists(current_month_payment_exists), then=Value("Yes")),
                default=Value("No")
            )
        )
        return students

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['batch'] = self.batch
        context['date_time'] = timezone.now().replace(day=1)
        context['students'] = self.get_queryset()
        return context


class StudentListFilter(ListAPIView):
    # serializer_class = PaymentSerializer
    pagination_class = CustomPagination

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

        if q_batch:
            students = students.filter(batch_id=q_batch)

        students = students.filter().select_related('batch').select_related('hsc_batch').annotate(
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
            latest_payment=Subquery(
                Payment.objects.filter(student=OuterRef('pk')).values('student').annotate(
                    total=Max('payment_date')
                ).values('total')
            ),
            due_amount=Coalesce(F('total_course_amount'), Value(0)) -
            Coalesce(F('total_discount'), Value(0)) -
            Coalesce(F('total_payment'), Value(0)),

            paid_current_month=Case(
                When(Exists(current_month_payment_exists), then=Value(True)),
                default=Value(False)
            )).values('id', 'name', 'phone', 'student_roll', 'hsc_batch__year', 'total_course_amount', 'total_discount', 'total_payment', 'paid_current_month', 'due_amount', 'batch__name', 'batch__start_time', 'batch__end_time', 'latest_payment')

        filter_by = self.request.query_params.get('filter_by', None)
        sort_by = self.request.query_params.get('sort_by', '')

        if filter_by and filter_by is not None:
            students = students.order_by(f"{sort_by}{filter_by}")

        # data = {"name": "Sort by name",
        #         "batch__name": "Sort by batch", "hsc_batch__year": "Sort by HSC", "due_amount": "Sort by due amount", "paid_current_month": "Sort by current month"}

        return students

    def list(self, request, *args, **kwargs):
        print(request.query_params.get('page', None))
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


class PracticeView(APIView):
    def get(self, request, *args, **kwargs):
        days = int(request.query_params.get('days')) + 1

        current_month = timezone.now().replace(day=1)

        current_month_payment_exists = Payment.objects.filter(
            student=OuterRef('pk'),
            payment_date__gte=current_month).values('id')[:1]

        d = Discount.objects.aggregate(
            total=Sum('discount_amount'),
            average=Avg('discount_amount'),
        )
        p = Payment.objects.annotate(month=TruncYear('payment_date')).values('month').annotate(
            total=Sum('payment_amount'))

        subquery1 = StudentEnroll.objects.filter(student=OuterRef('id')).values(
            'student')

        subquery2 = Discount.objects.filter(
            student=OuterRef('id')).values('student')

        students2 = Student.objects.annotate(
            total_course_fee=Subquery(subquery1.annotate(
                total=Sum('course_fee')
            ).values('total')
            ),
            total_discount=Subquery(subquery2.annotate(
                total=Sum('discount_amount')
            ).values('total')
            ),
        ).values('id', 'name', 'total_discount', 'total_course_fee')

        return Response(data={'d': p, 'discount': 'students1', 'data': students2, 'total': []})


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
                Fee.objects.filter(student=OuterRef('pk')).values('student').annotate(
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

                return Response(data={"message": "Fill correctly all the required Field", "errors": serializer_data.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'status': 'failed', 'message': 'something went wrong', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentTemplateView(LoginRequiredMixin, TemplateView):
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
