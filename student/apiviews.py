
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import College, AcademicYear, Batch
from course.models import Course
from address.models import District
from .serializers import StudentSerializer
from rest_framework import status


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
