from rest_framework.serializers import ModelSerializer, Serializer
from .models import District
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class DistrictSerializer(ModelSerializer):
    class Meta:
        model = District
        exclude = ['created_at', 'updated_at']


class TestSerializer(Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=District.objects.all())])
    status = serializers.BooleanField(required=False)
    test = serializers.CharField(required=False)

    def create(self, validated_data):
        print('validate and create')
        return District.objects.create(**validated_data)
