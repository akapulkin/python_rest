from rest_framework import serializers
from django.contrib.auth.models import User
from django_rest.models import Employee, Department, Project, Task


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ('id', 'head_of_department', 'name')
        read_only_fields = ('id',)


class EmployeeModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ('id', 'username', 'first_name', 'last_name', 'birthdate', 'department')
        read_only_fields = ('id',)

    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')


class EmployeeSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=32)
    first_name = serializers.CharField(max_length=32)
    last_name = serializers.CharField(max_length=32)
    birthdate = serializers.DateField()
    department = serializers.IntegerField(allow_null=True, required=False)


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'project_manager', 'name', 'start_date', 'end_date')
        read_only_fields = ('id', 'start_date', 'end_date')


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 'executor', 'name', 'project', 'start_date', 'end_date', 'status')
        read_only_fields = ('id',)
