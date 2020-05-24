import pytest
from uuid import uuid4

from django.urls import reverse
from django_rest.models import Employee
from django.contrib.auth.models import User
from rest_framework.test import APIClient


PASSWORD = 'PASSWORD'


def get_employee(is_staff=False):
    data = {'username': str(uuid4()), 'password': PASSWORD, 'first_name': 'test_name',
                 'last_name': 'test_name', 'birthdate': '1988-12-12'}
    user = User.objects.create_user(
        username=data['username'], password=PASSWORD,
        is_active=True, is_staff=is_staff, is_superuser=is_staff)
    employee = Employee.objects.create(user=user, birthdate=data['birthdate'])
    return employee, data


def get_client(employee):
    api_client = APIClient()
    body = {'username': employee.user.username, 'password': PASSWORD}
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


@pytest.mark.django_db
def test_create_employee_success(admin_client):
    url = reverse('employee_create')
    body = {'username': 'gadjikkk',
            'password': 'gavanava',
            'first_name': 'Vagrant',
            'last_name': 'Himichkovich',
            'birthdate': '1979-12-05'}

    resp = admin_client.post(url, data=body, format='json')
    
    assert resp.status_code == 200
    assert resp.data['username'] == body['username']
    assert Employee.objects.filter(id=resp.data['id']).count()


@pytest.mark.django_db
def test_create_employee_already_exist(admin_client, admin_user):
    url = reverse('employee_create')
    employee, body = get_employee()
    resp = admin_client.post(url, data=body, format='json')

    assert resp.status_code == 409


@pytest.mark.django_db
def test_create_employee_blank_data(admin_client):
    url = reverse('employee_create')
    resp = admin_client.post(url, data={}, format='json')
    
    assert resp.status_code == 400


@pytest.mark.django_db
def test_create_employee_not_valid(admin_client):
    url = reverse('employee_create')
    body = {'username': 'test_name'}
    resp = admin_client.post(url, data=body, format='json')
    
    assert resp.status_code == 400


@pytest.mark.django_db
def test_create_employee_unauthorized():
    url = reverse('employee_create')
    _, body = get_employee()
    client = APIClient()
    resp = client.post(url, data=body, format='json')
    
    assert resp.status_code == 403


@pytest.mark.django_db
def test_get_employee_success(admin_client):
    employee, _ = get_employee()
    url = reverse('employee', args=(employee.id,))
    resp = admin_client.get(path=url)

    assert 200 == resp.status_code


@pytest.mark.django_db
def test_get_employee_no_permissions(client):
    employee, _ = get_employee()
    url = reverse('employee', args=(employee.id,))
    resp = client.get(path=url)
    
    assert resp.status_code == 403


@pytest.mark.django_db
def test_get_employee_owner_success():
    employee, _ = get_employee()
    client = get_client(employee)
    url = reverse('employee', args=(employee.id,))
    resp = client.get(path=url)

    assert resp.status_code == 200


@pytest.mark.django_db
def test_get_employee_object_does_not_exist(admin_client):
    employee_not_exist_pk = 999
    url = reverse('employee', args=(employee_not_exist_pk,))
    resp = admin_client.get(path=url)

    assert resp.status_code == 404


@pytest.mark.django_db
def test_get_employee_unauthorized():
    client = APIClient()
    employee, _ = get_employee()
    url = reverse('employee', args=(employee.id,))
    resp = client.get(path=url)

    assert resp.status_code == 403
