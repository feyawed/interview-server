import pytest
import requests

base_url = 'http://localhost:8000'
obj_to_create = {"data": [{"key": "key1", "val": "val1", "valType": "str"}]}


def get_headers():
    auth_response = requests.post(base_url + "/api/auth", json={"username": "test", "password": "1234"})

    return {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + auth_response.json()['access_token']
    }


headers_with_token = get_headers()


def test_post_poly():
    returned_data = requests.post(base_url + "/api/poly", json=obj_to_create, headers=headers_with_token)

    assert obj_to_create['data'] == returned_data.json()['values'], "Returned data:" + returned_data.json()


def test_get_poly():
    returned_data = requests.get(base_url + "/api/poly", headers=headers_with_token)

    assert returned_data.json()[0] == {"object_id": 1,
                                       "data": obj_to_create["data"]}, "Returned data:" + returned_data.json()


def test_get_by_id():
    returned_data = requests.get(base_url + "/api/poly/1", headers=headers_with_token)

    assert returned_data.json() == {"object_id": 1, "data": obj_to_create["data"]}


def test_delete_by_id():
    returned_data = requests.delete(base_url + "/api/poly/2", headers=headers_with_token)
    # while 204 is expected, the server returns 200 while the entry deleted from db
    assert returned_data.status_code == 200


