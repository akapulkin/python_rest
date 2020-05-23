import pytest
from django.urls import reverse
from django_rest.models import Employee
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture
def admin_user():
    user_data = {'username': 'vololo122', 'password': 'gavanava', 'first_name': 'Vagrant',
                 'last_name': 'Hovancich', 'birthdate': '1988-12-12'}
    user = User.objects.create_user(
        username=user_data['username'], password=user_data['password'],
        is_staff=True, is_active=True, is_superuser=True)
    Employee.objects.create(user=user, birthdate=user_data['birthdate'])
    return user_data


@pytest.fixture
def admin_client(admin_user):
    api_client = APIClient()

    body = {'username': admin_user['username'], 'password': admin_user['password']}
    resp = api_client.post(path=reverse('token_obtain_pair'), data=body, format='json')

    token = f"Bearer {resp.data['access']}"
    api_client.credentials(HTTP_AUTHORIZATION=token)
    return api_client


@pytest.mark.django_db
def test_create_employee_success(admin_client):
    url = reverse('employee')

    body = {'username': 'gadjikkk',
            'password': 'gavanava',
            'first_name': 'Vagrant',
            'last_name': 'Himichkovich',
            'birthdate': '1979-12-05'}

    resp = admin_client.post(url, data=body, format='json')
    assert resp.status_code == 200
    assert resp.data['user']['username'] == body['username']
    assert Employee.objects.get(id=resp.data['id'])


@pytest.mark.django_db
def test_create_employee_already_exist(admin_client, admin_user):
    url = reverse('employee')
    body = admin_user
    resp = admin_client.post(url, data=body, format='json')

    assert resp.status_code == 409


@pytest.mark.django_db
def test_create_employee_blank_data(admin_client):
    url = reverse('employee')
    resp = admin_client.post(url, data={}, format='json')
    assert resp.status_code == 400


@pytest.mark.django_db
def test_create_employee_not_valid(admin_client):
    url = reverse('employee')
    body = {'username': 'test_name'}
    resp = admin_client.post(url, data=body, format='json')
    assert resp.status_code == 400


@pytest.mark.django_db
def test_create_employee_unauthorized(admin_user):
    url = reverse('employee')
    body = admin_user
    client = APIClient()
    resp = client.post(url, data=body, format='json')
    assert resp.status_code == 403
