import pytest

from django.urls import reverse
from django_rest.models import Project
from rest_framework.test import APIClient
from tests.conftest import get_project


@pytest.mark.django_db
def test_create_project_success(admin_client):
    url = reverse('project_create')
    body = {'name': 'Logistic'}
    resp = admin_client.post(url, data=body, format='json')

    assert resp.status_code == 201
    assert resp.data['name'] == body['name']
    assert Project.objects.filter(id=resp.data['id']).count()


@pytest.mark.django_db
def test_create_project_already_exist(admin_client, admin_user):
    url = reverse('project_create')
    Project.objects.create(name='Logistic')
    not_unique_project = {'name': 'Logistic'}
    resp = admin_client.post(url, data=not_unique_project, format='json')

    assert resp.status_code == 400


@pytest.mark.django_db
def test_create_project_blank_data(admin_client):
    url = reverse('project_create')
    resp = admin_client.post(url, data={}, format='json')

    assert resp.status_code == 400


@pytest.mark.django_db
def test_create_project_not_valid(admin_client):
    url = reverse('project_create')
    body = {'project_manager': 'NOT_VALID_DATA'}
    resp = admin_client.post(url, data=body, format='json')

    assert resp.status_code == 400


@pytest.mark.django_db
def test_create_project_unauthorized():
    url = reverse('project_create')
    project = {'name': 'Logistic changes'}
    client = APIClient()
    resp = client.post(url, data=project, format='json')

    assert resp.status_code == 403


# GET_TESTS #######################################


@pytest.mark.django_db
def test_get_project_success(admin_client):
    project, _ = get_project()
    url = reverse('project', args=(project.id,))
    resp = admin_client.get(path=url)

    assert 200 == resp.status_code


@pytest.mark.django_db
def test_get_project_object_does_not_exist(admin_client):
    project_not_exist_pk = 999
    url = reverse('project', args=(project_not_exist_pk,))
    resp = admin_client.get(path=url)

    assert resp.status_code == 404


@pytest.mark.django_db
def test_get_project_unauthorized():
    client = APIClient()
    project, _ = get_project()
    url = reverse('project', args=(project.id,))
    resp = client.get(path=url)

    assert resp.status_code == 403


# PUT_TESTS #######################################


@pytest.mark.django_db
def test_put_project_success(admin_client):
    project, body = get_project()
    url = reverse('project', args=(project.id,))
    new_name = 'IT Project'
    body['name'] = new_name
    resp = admin_client.put(url, data=body, format='json')

    assert resp.status_code == 200
    assert resp.data['name'] == new_name


@pytest.mark.django_db
def test_put_project_not_valid(admin_client):
    project, body = get_project()
    url = reverse('project', args=(project.id,))
    body['project_manager'] = 'NOT_VALID_DATA'
    resp = admin_client.put(url, data=body, format='json')

    assert resp.status_code == 400


@pytest.mark.django_db
def test_put_project_object_does_not_exist(admin_client):
    project_not_exist_pk = 999
    _, valid_body = get_project()
    url = reverse('project', args=(project_not_exist_pk,))
    resp = admin_client.put(url, data=valid_body, format='json')

    assert resp.status_code == 404


@pytest.mark.django_db
def test_put_project_unauthorized():
    client = APIClient()
    project, valid_body = get_project()
    url = reverse('project', args=(project.id,))
    resp = client.put(url, data=valid_body, format='json')

    assert resp.status_code == 403


# PATCH_TESTS #######################################


@pytest.mark.django_db
def test_patch_project_success(admin_client):
    project, _ = get_project()
    url = reverse('project', args=(project.id,))
    patch_body = {'name': 'IT Project'}
    resp = admin_client.patch(url, data=patch_body, format='json')

    assert resp.status_code == 200
    assert resp.data['name'] == patch_body['name']


@pytest.mark.django_db
def test_patch_project_not_valid(admin_client):
    project, _ = get_project()
    url = reverse('project', args=(project.id,))
    not_valid_body = {'project_manager': 'NOT_VALID_DATA'}
    resp = admin_client.patch(url, data=not_valid_body, format='json')

    assert resp.status_code == 400


@pytest.mark.django_db
def test_patch_project_object_does_not_exist(admin_client):
    project_not_exist_pk = 999
    url = reverse('project', args=(project_not_exist_pk,))
    patch_body = {'name': 'IT Department'}
    resp = admin_client.patch(url, data=patch_body, format='json')

    assert resp.status_code == 404


@pytest.mark.django_db
def test_patch_project_unauthorized():
    client = APIClient()
    project, _ = get_project()
    url = reverse('project', args=(project.id,))
    patch_body = {'name': 'IT Department'}
    resp = client.patch(url, data=patch_body, format='json')

    assert resp.status_code == 403


# DELETE_TESTS #######################################


@pytest.mark.django_db
def test_delete_project_success(admin_client):
    project, _ = get_project()
    url = reverse('project', args=(project.id,))
    resp = admin_client.delete(path=url)

    assert 204 == resp.status_code


@pytest.mark.django_db
def test_delete_project_object_does_not_exist(admin_client):
    project_not_exist_pk = 999
    url = reverse('project', args=(project_not_exist_pk,))
    resp = admin_client.delete(path=url)

    assert resp.status_code == 404


@pytest.mark.django_db
def test_delete_project_unauthorized():
    client = APIClient()
    project, _ = get_project()
    url = reverse('project', args=(project.id,))
    resp = client.delete(path=url)

    assert resp.status_code == 403
