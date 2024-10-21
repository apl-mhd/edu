from rest_framework import serializers
from .models import Payment
from student.models import Student
from course.models import Batch, Course, StudentEnroll, StudentBilling, Discount
from django.db import transaction


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class CourseAssignSerializer(serializers.Serializer):
    student = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    batch = serializers.PrimaryKeyRelatedField(queryset=Batch.objects.all())
    discount = serializers.IntegerField(required=False, allow_null=True)
    payment_amount = serializers.IntegerField(required=False, allow_null=True)

    def create(self, validated_data):
        student = validated_data.get('student')
        course = validated_data.get('course')
        batch = validated_data.get('batch')

        discount = validated_data.get('discount')
        payment_amount = validated_data.get('payment_amount')

        with transaction.atomic():
            student_enroll = StudentEnroll.objects.create(
                student=student, course=course, course_fee=course.course_fee)

            if discount:
                billing = Discount.objects.create(
                    student=student, discount_amount=discount)

            if payment_amount:
                payment = Payment.objects.create(student=student,
                                                 payment_amount=payment_amount)

        return validated_data

    # def validate(self, data):
    #     try:
    #         student = Student.objects.get(pk=data['student'])
    #     except Student.DoesNotExist:
    #         raise serializers.ValidationError(
    #             {"student": "The student does not exists"})

    #     try:
    #         batch = Batch.objects.get(pk=data["batch"])
    #     except Batch.DoesNotExist:
    #         raise serializers.ValidationError(
    #             {"batch": "The batch does not exists"})
    #     try:
    #         course = Course.objects.get(pk=data["course"])
    #     except Course.DoesNotExist:
    #         raise serializers.ValidationError(
    #             {"batch": "The course does not exists"})

    #     return data
