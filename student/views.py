from django.utils import timezone
from django.db.models import (
    Case, When, Subquery, Sum, OuterRef, Exists, Value, F
)
from django.db.models.functions import Coalesce
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from django_xhtml2pdf.views import PdfMixin

from course.models import Payment, Discount, StudentEnroll
from .models import Student, Batch


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
