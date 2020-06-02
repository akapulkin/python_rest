import pytest
from uuid import uuid4

from django.urls import reverse
from django_rest.models import Employee, Project, Task, Department
from django.contrib.auth.models import User
from rest_framework.test import APIClient


def get_employee(is_staff=False):
    data = {'username': str(uuid4()), 'password': 'PASSWORD', 'first_name': 'test_name',
            'last_name': 'test_name', 'birthdate': '1988-12-12'}
    user = User.objects.create_user(
        username=data['username'], password='PASSWORD', first_name=data['first_name'],
        last_name=data['last_name'], is_active=True, is_staff=is_staff, is_superuser=is_staff)
    employee = Employee.objects.create(user=user, birthdate=data['birthdate'])
    return employee, data


def get_department():
    data = {'name': 'Financial department'}
    employee, _ = get_employee()
    department = Department.objects.create(name=data['name'], head_of_department=employee)
    return department, data


def get_project():
    data = {'name': 'Roll cages'}
    employee, _ = get_employee()
    project = Project.objects.create(name=data['name'], project_manager=employee)
    return project, data


def get_task():
    project, _ = get_project()
    data = {'name': 'Do something special', 'project': project.id, 'start_date': '2020-04-30',
            'end_date': '2020-05-31', 'status': 'new'}
    task = Task.objects.create(name=data['name'], project=project, end_date=data['end_date'],
                               start_date=data['start_date'],  status=data['status'])
    return task, data


def get_client(employee):
    api_client = APIClient()
    body = {'username': employee.user.username, 'password': 'PASSWORD'}
    resp = api_client.post(path=reverse('token_obtain_pair'), data=body, format='json')
    token = f"Bearer {resp.data['access']}"
    api_client.credentials(HTTP_AUTHORIZATION=token)
    return api_client


@pytest.fixture
def client():
    employee, _ = get_employee()
    api_client = get_client(employee)
    return api_client


@pytest.fixture
def admin_client():
    employee, _ = get_employee(is_staff=True)
    api_client = get_client(employee)
    return api_client
