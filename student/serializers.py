from rest_framework import serializers
from .models import Student


# class A(serializers.ModelSerializer):
#     class Meta:


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


# class StudentSerializer(serializers.Serializer):
#     name = serializers.CharField()
