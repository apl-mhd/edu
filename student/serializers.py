from rest_framework import serializers



class StudentSerializer(serializers.Serializer):
    name = serializers.CharField()


class StudentModelSerializer(serializers.Serializer):
    name = serializers.CharField()
    