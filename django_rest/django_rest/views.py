from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException, status, PermissionDenied
from django_rest.models import Employee
from django.contrib.auth.models import User
from django_rest.serializers import EmployeeSerializer, EmployeeModelSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class ObjectExistsException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Object already exists.'
    default_code = 'object_exists'


def employee_update(employee, request_data):
    employee.user.username = request_data.get('username', employee.user.username)
    employee.user.password = request_data.get('password', employee.user.password)
    employee.user.first_name = request_data.get('first_name', employee.user.first_name)
    employee.user.last_name = request_data.get('last_name', employee.user.last_name)
    employee.birthdate = request_data.get('birthdate', employee.birthdate)
    employee.save()
    return employee


def permission_check(request, employee):
    # TODO move to permission class
    if request.user.is_staff or request.user == employee.user:
        return True
    else:
        raise PermissionDenied


class EmployeeAPIView(APIView):

    @swagger_auto_schema(operation_description='Get Employee.',
                         responses={200: EmployeeModelSerializer()})
    def get(self, request, pk):

        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeModelSerializer(employee)
        if permission_check(request, employee):
            return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update Employee.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password', 'first_name', 'last_name', 'birthdate'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                'birthdate': openapi.Schema(type=openapi.TYPE_STRING)
            },
        )
    )
    def put(self, request, pk):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            employee = get_object_or_404(Employee, pk=pk)
            if employee:
                employee = employee_update(employee, serializer.data)
                employee_data = EmployeeModelSerializer(employee)
                if permission_check(request, employee):
                    return Response(employee_data.data)

    @swagger_auto_schema(
        operation_description="Partial update Employee.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                'birthdate': openapi.Schema(type=openapi.TYPE_STRING)
            },
        )
    )
    def patch(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeModelSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            employee = employee_update(employee, serializer.initial_data)
            employee_data = EmployeeModelSerializer(employee)
            if permission_check(request, employee):
                return Response(employee_data.data)


class EmployeesCreateAPIView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    @swagger_auto_schema(
        operation_description='Create Employee.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password', 'first_name', 'last_name', 'birthdate'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                'birthdate': openapi.Schema(type=openapi.TYPE_STRING)
            },
        )
    )
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user, created = User.objects.get_or_create(username=serializer.data['username'])
            if created:
                user.password = make_password(serializer.data['password'])
                user.first_name = serializer.data['first_name']
                user.last_name = serializer.data['last_name']
                employee = Employee.objects.create(
                    user=user,
                    birthdate=serializer.data['birthdate']
                )
                employee_data = EmployeeModelSerializer(employee)
                return Response(data=employee_data.data, status=200)
            else:
                message = 'User with username {} already used'.format(serializer.data['username'])
                raise ObjectExistsException(message)
