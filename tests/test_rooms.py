from flask.testing import FlaskClient
from tests.utils import login


def test_get_rooms(populated_client: FlaskClient):
    response = login(populated_client)
    assert b"Login successful." in response.data

    response = populated_client.get("/room/")
    assert response.status_code == 200
    data = response.data.decode()
    assert "Room_1" in data


def test_search_rooms(populated_client: FlaskClient):
    response = login(populated_client)
    assert b"Login successful." in response.data

    response = populated_client.get("/room/?q=om_2")
    assert response.status_code == 200
    data = response.data.decode()
    assert "Room_2" in data


def test_create_room():
    ...


def test_update_room():
    ...


def test_delete_room():
    ...
