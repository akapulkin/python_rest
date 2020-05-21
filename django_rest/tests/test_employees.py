import pytest
from django.urls import reverse
from django_rest.models import Employee
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture
def admin_client(api_client=APIClient()):
    user = User.objects.create_user(username='vololo122', password='gavanava', is_staff=True, is_active=True, is_superuser=True)
    Employee.objects.create(user=user, birthdate='1988-12-12')
    resp = api_client.post(path=reverse('token_obtain_pair'), data={'username': 'vololo122', 'password': 'gavanava'}, format='json')
    token = f"Bearer {resp.data['access']}"
    api_client.credentials(HTTP_AUTHORIZATION=token)
    return api_client


@pytest.mark.django_db
def test_get_employee(admin_client):
    url = reverse('employee_get', args='1')
    resp = admin_client.get(path=url, data={'pk': '1'})
    assert resp.status_code == 200


@pytest.mark.django_db
def test_create_employee_success(admin_client):

    body = {'username': 'gadjikkk', 'password': 'gavanava', 'first_name': 'dddd',
            'last_name': 'Kaddddvanchich', 'birthdate': '1979-12-05'}

    resp = admin_client.post(path=reverse('employee'), data=body, format='json')
    assert resp.status_code == 200


@pytest.mark.django_db
def test_create_employee_not_valid_data(admin_client):
    # bad birthadate data

    body = {'username': 'iokolo', 'password': 'gavanava', 'first_name': 'Gorge',
            'last_name': 'Kavanchich', 'birthdate': '1979-55-05'}

    resp = admin_client.post(path=reverse('employee'), data=body, format='json')
    assert resp.status_code == 400


@pytest.mark.django_db
def test_create_employee_empty_data(admin_client):
    resp = admin_client.post(path=reverse('employee'), data={}, format='json')
    assert resp.status_code == 400


@pytest.mark.django_db
def test_create_employee_unauthorized():

    body = {'username': 'vololwwo', 'password': 'gavanava', 'first_name': 'Gorge',
            'last_name': 'Kavanchich', 'birthdate': '1979-12-05'}

    resp = APIClient().post(path=reverse('employee'), data=body, format='json')
    assert resp.status_code == 403


@pytest.mark.django_db
def test_update_employee_success(admin_client):

    body = {'username': 'vololo122', 'password': 'gavanava', 'first_name': 'Goge',
            'last_name': 'Jokovich', 'birthdate': '1979-12-05'}

    resp = admin_client.put(path=reverse('employee'), data=body, format='json')
    assert resp.status_code == 200


@pytest.mark.django_db
def test_delete_employee_success(admin_client):
    body = {'username': 'vololo122'}
    resp = admin_client.delete(path=reverse('employee'), data=body, format='json')
    assert resp.status_code == 204

# TODO  create delete test on success user without permissions
