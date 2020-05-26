from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException, status, PermissionDenied
from django_rest.models import Employee
from django.contrib.auth.models import User
from django_rest.serializers import EmployeeSerializer, EmployeeModelSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from swagger import employee_swager


class ObjectExistsException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Object already exists.'
    default_code = 'object_exists'


class EmployeeAPIView(APIView):

    @swagger_auto_schema(operation_description='Get Employee.',
                         responses={200: EmployeeModelSerializer()})
    def get(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        self.permission_check(request, employee)
        serializer = EmployeeModelSerializer(employee)
        return Response(serializer.data)

    @swagger_auto_schema(
        # TODO: add responses
        operation_description="Update Employee.",
        request_body=employee_swager.put_schema
    )
    def put(self, request, pk):
        serializer = EmployeeSerializer(data=request.data)
        self.permission_check(request, employee)
        if serializer.is_valid(raise_exception=True):
            employee = get_object_or_404(Employee, pk=pk)
            self.employee_update(employee, serializer.data)
            employee_data = EmployeeModelSerializer(employee)
            return Response(employee_data.data)

    @swagger_auto_schema(
        # TODO: add responses
        operation_description='Partial update Employee.',
        request_body=employee_swager.patch_schema
    )
    def patch(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        self.permission_check(request, employee)
        serializer = EmployeeModelSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            self.employee_update(employee, serializer.initial_data)
            employee_data = EmployeeModelSerializer(employee)
            return Response(employee_data.data)

    @swagger_auto_schema(operation_description='Delete Employee.',
                         responses={204: EmployeeModelSerializer()})
    def delete(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        self.permission_check(request, employee)
        serializer = EmployeeModelSerializer(employee)
        employee.delete()
        return Response(serializer.data, status=204)

    @staticmethod
    def employee_update(employee, request_data):
        employee.user.username = request_data.get('username', employee.user.username)
        employee.user.password = request_data.get('password', employee.user.password)
        employee.user.first_name = request_data.get('first_name', employee.user.first_name)
        employee.user.last_name = request_data.get('last_name', employee.user.last_name)
        employee.birthdate = request_data.get('birthdate', employee.birthdate)
        employee.save()

    @staticmethod
    def permission_check(request, employee):
        # TODO move to permission class
        if not request.user.is_staff and request.user != employee.user:
            raise PermissionDenied


class EmployeesCreateAPIView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    @swagger_auto_schema(
        # TODO: add responses
        operation_description='Create Employee.',
        request_body=employee_swager.post_schema
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
