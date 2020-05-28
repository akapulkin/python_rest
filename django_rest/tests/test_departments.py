import pytest
from uuid import uuid4

from django.urls import reverse
from django_rest.models import Employee, Department
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
    employee.department = department
    employee.save()
    return department, data


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


@pytest.mark.django_db
def test_create_department_success(admin_client):
    url = reverse('department_create')
    body = {'name': 'Logistic'}
    resp = admin_client.post(url, data=body, format='json')

    assert resp.status_code == 201
    assert resp.data['name'] == body['name']
    assert Department.objects.filter(id=resp.data['id']).count()


@pytest.mark.django_db
def test_create_department_already_exist(admin_client, admin_user):
    url = reverse('department_create')
    Department.objects.create(name='Logistic')
    not_unique_department = {'name': 'Logistic'}
    resp = admin_client.post(url, data=not_unique_department, format='json')

    assert resp.status_code == 400


@pytest.mark.django_db
def test_create_department_blank_data(admin_client):
    url = reverse('department_create')
    resp = admin_client.post(url, data={}, format='json')

    assert resp.status_code == 400


@pytest.mark.django_db
def test_create_department_not_valid(admin_client):
    url = reverse('department_create')
    body = {'head_of_department': 'NOT_VALID_DATA'}
    resp = admin_client.post(url, data=body, format='json')

    assert resp.status_code == 400


@pytest.mark.django_db
def test_create_department_unauthorized():
    url = reverse('department_create')
    department = {'name': 'Logistic'}
    client = APIClient()
    resp = client.post(url, data=department, format='json')

    assert resp.status_code == 403


# GET_TESTS #######################################


@pytest.mark.django_db
def test_get_department_success(admin_client):
    department, _ = get_department()
    url = reverse('department', args=(department.id,))
    resp = admin_client.get(path=url)

    assert 200 == resp.status_code


@pytest.mark.django_db
def test_get_department_no_permissions(client):
    department, _ = get_department()
    url = reverse('department', args=(department.id,))
    resp = client.get(path=url)

    assert resp.status_code == 403


@pytest.mark.django_db
def test_get_department_object_does_not_exist(admin_client):
    department_not_exist_pk = 999
    url = reverse('department', args=(department_not_exist_pk,))
    resp = admin_client.get(path=url)

    assert resp.status_code == 404


@pytest.mark.django_db
def test_get_department_unauthorized():
    client = APIClient()
    department, _ = get_department()
    url = reverse('department', args=(department.id,))
    resp = client.get(path=url)

    assert resp.status_code == 403


# PUT_TESTS #######################################


@pytest.mark.django_db
def test_put_department_success(admin_client):
    department, body = get_department()
    url = reverse('department', args=(department.id,))
    new_name = 'IT Department'
    body['name'] = new_name
    resp = admin_client.put(url, data=body, format='json')

    assert resp.status_code == 200
    assert resp.data['name'] == new_name


@pytest.mark.django_db
def test_put_department_not_valid(admin_client):
    department, body = get_department()
    url = reverse('department', args=(department.id,))
    body['head_of_department'] = 'NOT_VALID_DATA'
    resp = admin_client.put(url, data=body, format='json')

    assert resp.status_code == 400


@pytest.mark.django_db
def test_put_department_no_permissions(client):
    department, valid_body = get_department()
    url = reverse('department', args=(department.id,))
    resp = client.put(url, data=valid_body, format='json')

    assert resp.status_code == 403


@pytest.mark.django_db
def test_put_department_object_does_not_exist(admin_client):
    department_not_exist_pk = 999
    _, valid_body = get_department()
    url = reverse('department', args=(department_not_exist_pk,))
    resp = admin_client.put(url, data=valid_body, format='json')

    assert resp.status_code == 404


@pytest.mark.django_db
def test_put_department_unauthorized():
    client = APIClient()
    department, valid_body = get_department()
    url = reverse('department', args=(department.id,))
    resp = client.put(url, data=valid_body, format='json')

    assert resp.status_code == 403


# PATCH_TESTS #######################################


@pytest.mark.django_db
def test_patch_department_success(admin_client):
    department, _ = get_department()
    url = reverse('department', args=(department.id,))
    patch_body = {'name': 'IT Department'}
    resp = admin_client.patch(url, data=patch_body, format='json')

    assert resp.status_code == 200
    assert resp.data['name'] == patch_body['name']


@pytest.mark.django_db
def test_patch_department_not_valid(admin_client):
    department, _ = get_department()
    url = reverse('department', args=(department.id,))
    not_valid_body = {'head_of_department': 'NOT_VALID_DATA'}
    resp = admin_client.patch(url, data=not_valid_body, format='json')

    assert resp.status_code == 400


@pytest.mark.django_db
def test_patch_department_no_permissions(client):
    department, _ = get_department()
    url = reverse('department', args=(department.id,))
    patch_body = {'name': 'IT Department'}
    resp = client.patch(url, data=patch_body, format='json')

    assert resp.status_code == 403


@pytest.mark.django_db
def test_patch_department_object_does_not_exist(admin_client):
    department_not_exist_pk = 999
    url = reverse('department', args=(department_not_exist_pk,))
    patch_body = {'name': 'IT Department'}
    resp = admin_client.patch(url, data=patch_body, format='json')

    assert resp.status_code == 404


@pytest.mark.django_db
def test_patch_department_unauthorized():
    client = APIClient()
    department, _ = get_department()
    url = reverse('department', args=(department.id,))
    patch_body = {'name': 'IT Department'}
    resp = client.patch(url, data=patch_body, format='json')

    assert resp.status_code == 403


# DELETE_TESTS #######################################


@pytest.mark.django_db
def test_delete_department_success(admin_client):
    department, _ = get_department()
    url = reverse('department', args=(department.id,))
    resp = admin_client.delete(path=url)

    assert 204 == resp.status_code


@pytest.mark.django_db
def test_delete_department_no_permissions(client):
    department, _ = get_department()
    url = reverse('department', args=(department.id,))
    resp = client.delete(path=url)

    assert resp.status_code == 403


@pytest.mark.django_db
def test_delete_department_object_does_not_exist(admin_client):
    department_not_exist_pk = 999
    url = reverse('department', args=(department_not_exist_pk,))
    resp = admin_client.delete(path=url)

    assert resp.status_code == 404


@pytest.mark.django_db
def test_delete_department_unauthorized():
    client = APIClient()
    department, _ = get_department()
    url = reverse('department', args=(department.id,))
    resp = client.delete(path=url)

    assert resp.status_code == 403
