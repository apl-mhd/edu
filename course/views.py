from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import NotFound

from course.models import Payment
from student.models import Student
from .serializers import (
    PaymentSerializer,
    CourseAssignSerializer,
    CourseSerializer
)

class CourseView(ListAPIView):
    queryset = Student.objects.all()
    serailizer = CourseSerializer


class PaymentView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = PaymentSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Payment Successfull", "data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                return Response({"message": "Payment Error", "data": serializer.errors}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"message": 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, requset, *args, **kwargs):

        return Response(data={"message": "success"}, status=status.HTTP_200_OK)


class CourseAssingView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = CourseAssignSerializer(data=request.data)
            print(request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data={"message": "Successfully course assigned", "data": "serializer.data"}, status=status.HTTP_201_CREATED)

            else:
                return Response({"message": "Validation Error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, requset, *args, **kwargs):

        return Response(data={"message": "success"}, status=status.HTTP_200_OK)


class StudentPaymentListView(ListAPIView):

    serializer_class = PaymentSerializer

    def get_queryset(self, *args, **kwargs):
        studend_id = self.kwargs.get('id')
        try:
            return Payment.objects.filter(student=studend_id)

        except Student.DoesNotExist:
            raise NotFound(detail="Student not found")
