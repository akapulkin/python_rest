from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.views import APIView
from django_rest.models import Employee
from django.contrib.auth.models import User
from django_rest.serializers import EmployeeGetSerializer, EmployeeSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class EmployeeViewAPI(APIView):  #genericview
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        """
        Return a list of Employees.
        """
        user = get_object_or_404(User, username=request.data['username'])
        serializer = EmployeeGetSerializer(Employee.objects.get(user=user))
        return Response(serializer.data)

    def post(self, request):
        """
        Create Employee.
        """
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

    def put(self, request):
        """
        Update employee data.
        """
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

    def delete(self, request):
        """
        Delete employee data.
        """
        data = request.data.get('employee')
        user = get_object_or_404(User, username=data['username'])
        user.delete()
        return Response({"message": "Employee with username `{}` has been deleted.".format(data['username'])}, status=204)

#
# class DepartmentViewAPI(APIView):
#     permission_classes = (IsAuthenticated, IsAdminUser)
#
#     def get(self, request):
#         """
#         Return a list of Departments.
#         """
#         queryset = Department.objects.all()
#         serializer = DepartmentSerializer(queryset, many=True)
#         return Response({"departmets": serializer.data})
#
#     def post(self, request):
#         """
#         Create Employee.
#         """
#         department = request.data.get("department")
#         serializer = DepartmentSerializer(data=department)
#         if serializer.is_valid(raise_exception=True):
#             department_saved = serializer.save()
#             return Response({"success": "Department '{}' created successfully".format(department_saved.name)})
#
#     def put(self, request):
#         """
#         Update employee data.
#         """
#         data = request.data.get('department')
#         department = get_object_or_404(Department, username=data['name'])
#         serializer = EmployeeSerializer(instance=department, data=data, partial=True)
#         if serializer.is_valid(raise_exception=True):
#             department_saved = serializer.save()
#         return Response({"success": "Employee '{}' updated successfully".format(department_saved.user.username)})
#
#     def delete(self, request):
#         """
#         Delete employee data.
#         """
#         data = request.data.get('department')
#         user = get_object_or_404(User, username=data['name'])
#         user.delete()
#         return Response({"message": "Department with name `{}` has been deleted.".format(data['username'])}, status=204)