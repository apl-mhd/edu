from rest_framework import serializers
from .models import Payment
from student.models import Student, Batch
from course.models import Course, StudentEnroll, Fee, Discount
from django.db import transaction


class CourseSerializer(serializers.ModelSerializer):
     class Meta:
        model = Course
        fields = "__all__"

class CourseSerializer2(serializers.ModelSerializer):
     class Meta:
        model = Course
        fields = ["name"]

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class CourseAssignSerializer(serializers.Serializer):
    student = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    discount_amount = serializers.IntegerField(
        min_value=1, required=False, allow_null=True)
    payment_amount = serializers.IntegerField(
        min_value=1, required=False, allow_null=True)

    def create(self, validated_data):
        student = validated_data.get('student')
        course = validated_data.get('course')

        discount_amount = validated_data.get('discount_amount')
        payment_amount = validated_data.get('payment_amount')

        with transaction.atomic():
            student_enroll = StudentEnroll.objects.create(
                student=student, course=course, course_fee=course.course_fee)

            if discount_amount:
                billing = Discount.objects.create(
                    student=student, discount_amount=discount_amount)

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
