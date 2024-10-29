from rest_framework import serializers
from .models import Student, Batch, AcademicYear, District


# class A(serializers.ModelSerializer):
#     class Meta:


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model: Batch
        fields = '__all__'


class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model: AcademicYear
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model: District
        fields = '__all__'


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model: Batch
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


# class StudentSerializer(serializers.Serializer):
#     name = serializers.CharField()
