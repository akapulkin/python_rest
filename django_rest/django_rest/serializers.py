from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404

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


#
# class DepartmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Department
#         fields = ('id', 'name', 'head_of_department')
#
#     class Meta:
#         model = Department
#         fields = ['employee', 'name']
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Employer` instance, given the validated data.
#         """
#         user = get_object_or_404(User, username=validated_data['username'])
#         return Department.objects.create(user=user, birthdate=validated_data['name'])
#
#     def update(self, instance, validated_data):
#         instance.user.username = validated_data['username']
#         instance.user.password = validated_data['password']
#         instance.user.first_name = validated_data['first_name']
#         instance.user.last_name = validated_data['last_name']
#         instance.user.save()
#         instance.birthdate = validated_data['birthdate']
#
#         instance.save()
#         return instance
