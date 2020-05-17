import requests
import json
import pytest
from django.urls import reverse
from django.test.client import Client


@pytest.fixture
def get_token(client):
    resp = client.post(url=reverse('token_obtain_pair'), json={'username': 'vololo122', 'password': 'gavanava'})
    return f"Bearer {json.loads(resp.text)['access']}"


@pytest.mark.django_db
def test_get_employee(client):

    body = {'username': 'vololo122'}
    client = Client(Authorization=get_token())
    resp = client.get(url=reverse('employee'), json=body)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_create_employee_success():

    body = {'employee': {'username': 'gadjikkk', 'password': 'gavanava', 'first_name': 'Gorge',
                         'last_name': 'Kavanchich', 'birthdate': '1979-12-05'}}

    s = requests.Session()
    s.headers.update({'Authorization': get_token()})

    resp = s.post(url=reverse('employee'), json=body)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_create_employee_not_valid_data():

    body = {'employee': {'username': '*7?dsd±', 'password': 'gavanava', 'first_name': 'Gorge',
                         'last_name': 'Kavanchich', 'birthdate': '1979-55-05'}}

    s = requests.Session()
    s.headers.update({'Authorization': get_token()})

    resp = s.post(url=reverse('employee'), json=body)
    assert resp.status_code == 400


@pytest.mark.django_db
def test_create_employee_empty_data():

    body = {}

    s = requests.Session()
    s.headers.update({'Authorization': get_token()})

    resp = s.post(url, json=body)
    assert resp.status_code == 400


@pytest.mark.django_db
def test_create_employee_unauthorized():

    body = {'username': 'vololwwo', 'password': 'gavanava', 'first_name': 'Gorge',
            'last_name': 'Kavanchich', 'birthdate': '1979-12-05'}

    s = requests.Session()

    resp = s.post(url, json=body)
    assert resp.status_code == 403


@pytest.mark.django_db
def test_update_employee_success():

    body = {'username': 'vololo2332', 'password': 'gavanava', 'first_name': 'Goge',
            'last_name': 'Jokovich', 'birthdate': '1979-12-05'}

    s = requests.Session()
    s.headers.update({'Authorization': get_token()})

    resp = s.put(url, json=body)
    assert resp.status_code == 200


@pytest.mark.django_db
# TODO  create delete test on success user without permissions
def test_delete_employee_success():

    body = {'username': 'gadjikkk'}

    s = requests.Session()
    s.headers.update({'Authorization': get_token(s)})

    resp = s.delete(url, json=body)
    assert resp.status_code == 204
