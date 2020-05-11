import requests
import json

url = 'http://127.0.0.1:8002/employee/'


def get_token(session):
    resp = session.post(url='http://127.0.0.1:8002/api/token/', json={'username': 'vololo122', 'password': 'gavanava'})
    return f"Bearer {json.loads(resp.text)['access']}"


def test_create_employee_success():

    body = {'employee': {'username': 'vololo122', 'password': 'gavanava', 'first_name': 'Gorge',
                         'last_name': 'Kavanchich', 'birthdate': '1979-12-05'}}

    s = requests.Session()
    s.headers.update({'Authorization': get_token(s)})

    resp = s.post(url, json=body)
    assert resp.status_code == 200

    resp_body = resp.json()
    assert resp.url == url
    print(resp_body)


def test_create_employee_not_valid_data():

    body = {'employee': {'username': '*7?dsd±', 'password': 'gavanava', 'first_name': 'Gorge',
                         'last_name': 'Kavanchich', 'birthdate': '1979-55-05'}}

    s = requests.Session()
    s.headers.update({'Authorization': get_token(s)})

    resp = s.post(url, json=body)
    assert resp.status_code == 400

    resp_body = resp.json()
    assert resp.url == url
    print(resp_body)


def test_create_employee_empty_data():

    body = {}

    s = requests.Session()
    s.headers.update({'Authorization': get_token(s)})

    resp = s.post(url, json=body)
    assert resp.status_code == 400

    resp_body = resp.json()
    assert resp.url == url
    print(resp_body)


def test_create_employee_unauthorized():

    body = {'employee': {'username': 'vololo', 'password': 'gavanava', 'first_name': 'Gorge',
                         'last_name': 'Kavanchich', 'birthdate': '1979-12-05'}}

    s = requests.Session()

    resp = s.post(url, json=body)
    assert resp.status_code == 403

    resp_body = resp.json()
    assert resp.url == url
    print(resp_body)
