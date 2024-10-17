from django.shortcuts import render
from django.http import HttpResponse

from address.models import District, College
from course.models import Course, Payment, StudentBilling
from student.models import Student
import json
from .serializers import PaymentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
# Create your views here.
from django.db.models import Subquery, Sum, OuterRef, When, Case, Exists, Value, F
from django.utils import timezone


class PaymentView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            s = Student.objects.filter(pk=1).first()
            # request.data['student'] = 100
            serializer = PaymentSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Payment Successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                return Response({"message": "Validation Error", "data": serializer.errors}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"message": 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, requset, *args, **kwargs):

        return Response(data={"message": "success"}, status=status.HTTP_200_OK)
