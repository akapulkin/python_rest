import pytest
from uuid import uuid4

from django.urls import reverse
from django_rest.models import Employee, Project
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


def get_project():
    data = {'name': 'Roll cages'}
    employee, _ = get_employee()
    project = Project.objects.create(name=data['name'], project_manager=employee)
    return project, data


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
def test_get_project_no_permissions(client):
    project, _ = get_project()
    url = reverse('project', args=(project.id,))
    resp = client.get(path=url)

    assert resp.status_code == 403


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
def test_put_project_no_permissions(client):
    project, valid_body = get_project()
    url = reverse('project', args=(project.id,))
    resp = client.put(url, data=valid_body, format='json')

    assert resp.status_code == 403


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
def test_patch_project_no_permissions(client):
    project, _ = get_project()
    url = reverse('project', args=(project.id,))
    patch_body = {'name': 'IT Project'}
    resp = client.patch(url, data=patch_body, format='json')

    assert resp.status_code == 403


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
def test_delete_project_no_permissions(client):
    project, _ = get_project()
    url = reverse('project', args=(project.id,))
    resp = client.delete(path=url)

    assert resp.status_code == 403


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
