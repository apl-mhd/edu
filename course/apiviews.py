from rest_framework.generics import ListAPIView
from .models import Course
from .serializers import CourseSerializer


class CourseAPIView(ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        # name = self.request.GET.get('name', '')
        # courses = Course.objects.filter(name__icontains=name)[:10]
        return Course.objects.all()
