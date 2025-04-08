from django.utils import timezone
from django.db.models import (
    Q, When, Subquery, OuterRef, Sum, Case, Value, Exists, F, Max
)
from django.db.models.functions import Coalesce

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from address.models import District
from course.models import Course, Payment, StudentEnroll, Discount
from .models import College, AcademicYear, Batch, Student
from .serializers import StudentSerializer


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


class StudentListFilter(ListAPIView):
    pagination_class = CustomPagination

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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

        return students

    def list(self, request, *args, **kwargs):
        # print(request.query_params.get('page', None))
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(page)

        data = queryset
        return Response(data)


class StudentCreateView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            serializer_data = StudentSerializer(data=request.data)
            if serializer_data.is_valid():
                serializer_data.save()
                return Response({"message": "Successfully student created.", "data": serializer_data.data}, status=status.HTTP_201_CREATED)
            else:

                return Response({"message": "Fill correctly all the required Field", "errors": serializer_data.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'status': 'failed', 'message': 'something went wrong', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentDataFormAPIView(APIView):
    def get(self, request, *args, **kwargs):

        home_towns = District.objects.all().filter(status=True).values("id", "name")
        colleges = College.objects.all().values("id", "name")
        courses = Course.objects.all().values("id", "name", "course_fee")
        academic_years = AcademicYear.objects.all().values('id', 'year')
        batches = Batch.objects.all()
        batches = [{"id": i.id, "title": i.get_batch_details()}
                   for i in batches]

        return Response({
            "home_towns": home_towns,
            "colleges": colleges,
            "courses": courses,
            "academic_years": academic_years,
            "batches":  batches
        })


class StudentDetailView(RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
