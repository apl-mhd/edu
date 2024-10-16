from course.models import *
from student.models import *
from django.utils import timezone
from django.db.models import F, Q, Avg, Sum, Count, Subquery, OuterRef, Case, When, Value, CharField
from django.db import connection


def run():

    # current_month = timezone.now().replace(
    #     day=1, hour=0, minute=0, second=0, microsecond=0)

    # current_month_start = timezone.now().replace(
    #     day=1)  # Start of the current month

    # students = Student.objects.annotate(
    #     total_discounts=Sum('payments__discount'),
    #     total_payments=Sum('payments__payment'),
    #     total_course_amount=Sum('payments__course_amount'),
    #     paid_current_month=Case(
    #         When(
    #             Q(payments__created_at__gte=current_month_start) &
    #             Q(payments__payment__gt=0),
    #             then=Value('Yes')
    #         ),
    #         default=Value('No'),
    #         output_field=CharField()
    #     )
    # ).distinct()

    # print(students)
    # for i in students:
    #     print(
    #         f"{i.id} -- {i.total_discounts} -- {i.total_payments} -- {i.total_course_amount}")

# payment = Payment.objects.annotate(
#     current_month_payement=Case(
#         When(Q(created_at__gte=current_month) &
#              Q(payment__gt=0), then=Value('Yes')),
#         default=Value('No')
#     )
# ).values('student_id').distinct()

# stu_payment = Student.objects.annotate(
#     current_month_payment=Case(
#         When(
#             Q(payments__created_at__gte=current_month) &
#             Q(payments__payment__gt=0), then=Value('Yes')
#         ),
#         # default=Value("No"),
#         output_field=CharField()
#     )
# ).distinct()

# .annotate(
#     current_month_payement=Case(
#         When(Q(created_at__gte=current_month) &
#              Q(payment__gt=0), then=Value('Yes')),
#         default=Value('No')
#     )
# ).values('student_id').distinct()

# for i in payment:
#     print(f"{i['id']}---{i['current_month_payement']}")

# payment = Payment.objects.values('student_id').filter(
#     Q(created_at__gte=current_month) & Q(payment__gt=0)
# )
# payment = Payment.objects.filter(
#     Q(created_at__gte=current_month) & Q(payment__gt=0)
# ).values('student_id').distinct()

# sub = Payment.objects.filter(Q(student_id__in=Subquery(
#     payment))).annotate(total_payment=Sum('payment'))

# Payment.objects.annotate(a=Sum('payment'))

# print(connection.queries)
