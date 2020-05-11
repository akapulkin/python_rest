from rest_framework.response import Response
from rest_framework.views import APIView
from django_rest.models import Employee
from django_rest.serialyzers import EmployeeSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class EmployeeViewAPI(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        """
        Return a list of Employees.
        """
        queryset = Employee.objects.all()
        serializer = EmployeeSerializer(queryset, many=True)
        return Response({"employee": serializer.data})

    def post(self, request):
        """
        Create Employee.
        """
        employeer = request.data.get("employee")
        serializer = EmployeeSerializer(data=employeer)
        if serializer.is_valid(raise_exception=True):
            employee_saved = serializer.save()
            if type(employee_saved) is not str:
                return Response({"success": "Employee '{}' created successfully".format(employee_saved.user.username)})
            else:
                return Response({"error": "Employee '{}' not created".format(employee_saved)})
