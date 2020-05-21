from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.views import APIView
from django_rest.models import Employee
from django.contrib.auth.models import User
from django_rest.serializers import EmployeeGetSerializer, EmployeeSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class EmployeeGetViewAPI(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    @swagger_auto_schema(operation_description="Create Employee.",
                         responses={200: EmployeeGetSerializer(many=True)})
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = EmployeeGetSerializer(Employee.objects.get(user=user))
        return Response(serializer.data)


class EmployeesViewAPI(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    @swagger_auto_schema(
        operation_description="Create Employee.",
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
        ),
        security=[]
    )
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user, created = User.objects.get_or_create(username=serializer.data['username'])
            if created:
                user.password = make_password(serializer.data['password'])
                user.first_name = serializer.data['first_name']
                user.last_name = serializer.data['last_name']
                user.save()
                employee = Employee.objects.create(user=user, birthdate=serializer.data['birthdate']).save()
                return Response({"success": "Employee '{}' created successfully".format(employee)}, status=200)
            else:
                return Response({"error": "This username: '{}' already used".format(serializer.data['username'])}, status=409)

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
        ),
        security=[]
    )
    def put(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(User, username=serializer.data['username'])
            if user:
                employee = get_object_or_404(Employee, user=user)
                employee.user.password = serializer.data['username']
                employee.user.first_name = serializer.data['first_name']
                employee.user.last_name = serializer.data['last_name']
                employee.birthdate = serializer.data['birthdate']
                employee.save()
                return Response({"success": "Employee '{}' updated successfully".format(employee)})

    @swagger_auto_schema(
        operation_description="Delete Employee.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        security=[]
    )
    def delete(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        user.delete()
        return Response({"message": "Employee with username `{}` has been deleted.".format(request.data['username'])}, status=204)
