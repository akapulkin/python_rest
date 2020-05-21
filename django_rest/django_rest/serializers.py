from django_rest.models import Employee
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class EmployeeGetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = ['user', 'birthdate']


class EmployeeSerializer(serializers.Serializer):

    username = serializers.CharField(required=True, max_length=32)
    password = serializers.CharField(required=True, max_length=32)
    first_name = serializers.CharField(max_length=32)
    last_name = serializers.CharField(max_length=32)
    birthdate = serializers.DateField()

