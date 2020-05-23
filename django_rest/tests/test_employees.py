import pytest
from django.urls import reverse
from django_rest.models import Employee
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture
def admin_user():
    user = User.objects.create_user(username='vololo122', password='gavanava', is_staff=True,
                                    is_active=True, is_superuser=True)
    return Employee.objects.create(user=user, birthdate='1988-12-12')


@pytest.fixture
def admin_client(admin_user):
    api_client = APIClient()

    body = {'username': admin_user.user.username, 'password': admin_user.user.password}
    resp = api_client.post(path=reverse('token_obtain_pair'), data=body, format='json')

    token = f"Bearer {resp.data['access']}"
    api_client.credentials(HTTP_AUTHORIZATION=token)
    return api_client


@pytest.mark.django_db
def test_create_employee_success(admin_client):
    url = reverse('employee')

    body = {'username': 'gadjikkk', 'password': 'gavanava', 'first_name': 'dddd',
            'last_name': 'Kaddddvanchich', 'birthdate': '1979-12-05'}

    resp = admin_client.post(url, data=body, format='json')
    assert resp.status_code == 200
    # 1. response[body][username] == body[username]
    # 2. Employee.objects.get(id=response[body][id])
    # assert body['username'] == Employee.objects.get(user__username=body['username']).user.username


@pytest.mark.django_db
def test_create_employee_already_exist(admin_client, admin_user):
    url = reverse('employee')
    body = {
        'username': admin_user.user.username,
        'password': admin_user.user.password,
        'first_name': admin_user.user.first_name,
        'last_name': admin_user.user.last_name,
        'birthdate': admin_user.birthdate
    }
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
def test_create_employee_unauthorized():
    url = reverse('employee')
    body = {'username': 'gadjikkk', 'password': 'gavanava', 'first_name': 'dddd',
            'last_name': 'Kaddddvanchich', 'birthdate': '1979-12-05'}
    client = APIClient()
    resp = client.post(url, data=body, format='json')
    assert resp.status_code == 401
