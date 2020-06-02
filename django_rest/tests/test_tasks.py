import pytest

from django.urls import reverse
from django_rest.models import Task
from rest_framework.test import APIClient
from tests.conftest import get_task


@pytest.mark.django_db
def test_create_task_success(admin_client):
    url = reverse('task_create')
    task, _ = get_task()
    body = {'name': 'Do something special', 'project': task.project.id,
            'start_date': '2020-05-30', 'end_date': '2020-07-31', 'status': 'new'}
    resp = admin_client.post(url, data=body, format='json')

    assert resp.status_code == 201
    assert resp.data['name'] == body['name']
    assert Task.objects.filter(id=resp.data['id']).count()


@pytest.mark.django_db
def test_create_task_blank_data(admin_client):
    url = reverse('task_create')
    resp = admin_client.post(url, data={}, format='json')

    assert resp.status_code == 400


@pytest.mark.django_db
def test_create_task_not_valid(admin_client):
    url = reverse('task_create')
    body = {'executor': 'NOT_VALID_DATA'}
    resp = admin_client.post(url, data=body, format='json')

    assert resp.status_code == 400


@pytest.mark.django_db
def test_create_task_unauthorized():
    url = reverse('task_create')
    task = {'name': 'Logistic changes'}
    client = APIClient()
    resp = client.post(url, data=task, format='json')

    assert resp.status_code == 403


# GET_TESTS #######################################


@pytest.mark.django_db
def test_get_task_success(admin_client):
    task, _ = get_task()
    url = reverse('task', args=(task.id,))
    resp = admin_client.get(path=url)

    assert 200 == resp.status_code


@pytest.mark.django_db
def test_get_task_object_does_not_exist(admin_client):
    task_not_exist_pk = 999
    url = reverse('task', args=(task_not_exist_pk,))
    resp = admin_client.get(path=url)

    assert resp.status_code == 404


@pytest.mark.django_db
def test_get_task_unauthorized():
    client = APIClient()
    task, _ = get_task()
    url = reverse('task', args=(task.id,))
    resp = client.get(path=url)

    assert resp.status_code == 403


# PUT_TESTS #######################################


@pytest.mark.django_db
def test_put_task_success(admin_client):
    task, body = get_task()
    url = reverse('task', args=(task.id,))
    new_name = 'IT Task'
    body['name'] = new_name
    resp = admin_client.put(url, data=body, format='json')

    assert resp.status_code == 200
    assert resp.data['name'] == new_name


@pytest.mark.django_db
def test_put_task_not_valid(admin_client):
    task, body = get_task()
    url = reverse('task', args=(task.id,))
    body['executor'] = 'NOT_VALID_DATA'
    resp = admin_client.put(url, data=body, format='json')

    assert resp.status_code == 400


@pytest.mark.django_db
def test_put_task_object_does_not_exist(admin_client):
    task_not_exist_pk = 999
    _, valid_body = get_task()
    url = reverse('task', args=(task_not_exist_pk,))
    resp = admin_client.put(url, data=valid_body, format='json')

    assert resp.status_code == 404


@pytest.mark.django_db
def test_put_task_unauthorized():
    client = APIClient()
    task, valid_body = get_task()
    url = reverse('task', args=(task.id,))
    resp = client.put(url, data=valid_body, format='json')

    assert resp.status_code == 403


# PATCH_TESTS #######################################


@pytest.mark.django_db
def test_patch_task_success(admin_client):
    task, _ = get_task()
    url = reverse('task', args=(task.id,))
    patch_body = {'name': 'IT Task'}
    resp = admin_client.patch(url, data=patch_body, format='json')

    assert resp.status_code == 200
    assert resp.data['name'] == patch_body['name']


@pytest.mark.django_db
def test_patch_task_not_valid(admin_client):
    task, _ = get_task()
    url = reverse('task', args=(task.id,))
    not_valid_body = {'executor': 'NOT_VALID_DATA'}
    resp = admin_client.patch(url, data=not_valid_body, format='json')

    assert resp.status_code == 400


@pytest.mark.django_db
def test_patch_task_object_does_not_exist(admin_client):
    task_not_exist_pk = 999
    url = reverse('task', args=(task_not_exist_pk,))
    patch_body = {'name': 'IT task'}
    resp = admin_client.patch(url, data=patch_body, format='json')

    assert resp.status_code == 404


@pytest.mark.django_db
def test_patch_task_unauthorized():
    client = APIClient()
    task, _ = get_task()
    url = reverse('task', args=(task.id,))
    patch_body = {'name': 'IT Task'}
    resp = client.patch(url, data=patch_body, format='json')

    assert resp.status_code == 403


# DELETE_TESTS #######################################


@pytest.mark.django_db
def test_delete_task_success(admin_client):
    task, _ = get_task()
    url = reverse('task', args=(task.id,))
    resp = admin_client.delete(path=url)

    assert 204 == resp.status_code


@pytest.mark.django_db
def test_delete_task_object_does_not_exist(admin_client):
    task_not_exist_pk = 999
    url = reverse('task', args=(task_not_exist_pk,))
    resp = admin_client.delete(path=url)

    assert resp.status_code == 404


@pytest.mark.django_db
def test_delete_task_unauthorized():
    client = APIClient()
    task, _ = get_task()
    url = reverse('task', args=(task.id,))
    resp = client.delete(path=url)

    assert resp.status_code == 403
