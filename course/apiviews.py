from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
# from django_filters.rest_framework import DjangoFilterBackend
from .models import Course
from .serializers import CourseSerializer, CourseSerializer2


class CustomPagination(PageNumberPagination):
    page_size = 2  # Number of records per page
    page_size_query_param = 'page_size'
    max_page_size = 100

    def __init__(self, page_seize=2):
        self.page_size = page_seize

    def get_paginated_response(self, data):
        return Response({
            "count": self.page.paginator.count,
            "total_pages": self.page.paginator.num_pages,
            "current_page": self.page.number,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "data": data  # Rename "results" to "data"
        })


class CourseAPIView(APIView):

    def get(self, request):
        print(request.query_params.get('name', None))
        print(request.query_params.get('page', None))
        print(self.request.GET.get('name'))
        query_set = Course.objects.all()
        paginator = CustomPagination(page_seize=2)
        paginated_queryset = paginator.paginate_queryset(query_set, request)
        serializer = CourseSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

        return Response(data=serialize.data)

    # def get_queryset(self):

    #     name = self.request.GET.get('name', '')

    #     courses = Course.objects.filter(name__icontains=name)[:10]

    #     return courses


class _CourseAPIView(ListAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["a"] = {"a": "a"}
        return context

    # def get_serializer_class(self):
    #     return CourseSerializer2

    # def get_queryset(self):
    #     queryset = Course.objects.all()
    #     return queryset

    # def list(self, request):
    #     queryset = self.get_queryset()
    #     serializer = CourseSerializer(queryset, many=True)
    #     return Response(data=queryset.values())


class _CourseAPIView(ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):

        name = self.request.GET.get('name', '')

        courses = Course.objects.filter(name__icontains=name)[:10]

        return courses
