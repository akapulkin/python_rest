from django_rest.models import Employee
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class EmployeeModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ['id', 'username', 'first_name', 'last_name', 'birthdate']

    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')


class EmployeeSerializer(serializers.Serializer):

    username = serializers.CharField(required=True, max_length=32)
    password = serializers.CharField(required=True, max_length=32)
    first_name = serializers.CharField(max_length=32)
    last_name = serializers.CharField(max_length=32)
    birthdate = serializers.DateField()

