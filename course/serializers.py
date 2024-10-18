from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class CourseAssignSerializer(serializers.ModelSerializer):
    student = serializers.IntegerField()
    batch = serializers.IntegerField()
    start_time = serializers.TimeField()
    discount = serializers.IntegerField()
    amount_payment = serializers.IntegerField()
