import pytest

from django.urls import reverse
from django_rest.models import Department
from rest_framework.test import APIClient
from tests.conftest import get_department


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
