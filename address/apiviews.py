from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from .models import District
from .serializers import DistrictSerializer, TestSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.filters import SearchFilter, OrderingFilter
import json


class DistrictListAPIView(ListAPIView):
    """
    API view to retrieve a list of districts.

    - Supports searching by district name.
    - Uses Django Rest Framework's ListAPIView.
    - Allows partial matches when searching by name.
    """

    model = District
    queryset = District.objects.all()
    serializer_class = TestSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class DistrictCreateView(CreateAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class DistrictUpdateView(UpdateAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class DistrictDeleteView(DestroyAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


def test(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        serializer = TestSerializer(data=data)
        if serializer.is_valid():
            if serializer.save():
                return JsonResponse(serializer.errors, status=400)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)