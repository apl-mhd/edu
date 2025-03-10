
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import College, AcademicYear, Batch
from course.models import Course
from address.models import District


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
