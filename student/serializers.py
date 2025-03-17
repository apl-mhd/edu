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
        # fields = '__all__'
        exclude = ['created_at', 'updated_at']

        read_only_fields = ['student_roll']

    def create(self, validated_data):

        hsc_batch = validated_data['hsc_batch']

        student = Student.objects.filter(
            hsc_batch=hsc_batch).order_by('-id').first()

        if student:
            last_roll = student.student_roll
            student_roll = last_roll+1
        else:
            student_roll = int(str(hsc_batch.year % 100)+str("0001"))

        validated_data['student_roll'] = student_roll

        return super().create(validated_data)


# class StudentSerializer(serializers.Serializer):
#     name = serializers.CharField()
