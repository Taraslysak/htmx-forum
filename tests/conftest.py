import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app, db
from app import models as m
from tests.utils import login, register


@pytest.fixture()
def app():
    app = create_app("testing")
    app.config.update(
        {
            "TESTING": True,
        }
    )

    yield app


@pytest.fixture()
def client(app: Flask):
    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()

        db.drop_all()
        db.create_all()
        register()
        login(client)

        yield client
        db.drop_all()
        app_ctx.pop()


@pytest.fixture()
def runner(app, client):
    from app import commands

    commands.init(app)

    yield app.test_cli_runner()


@pytest.fixture
def populated_client(client: FlaskClient):
    NUM_TEST_USERS = 100
    for i in range(NUM_TEST_USERS):
        m.User(
            username=f"user{i+1}",
            email=f"user{i+1}@mail.com",
            password="password",
        ).save(False)
    NUM_TEST_ROOMS = 10
    for i in range(NUM_TEST_ROOMS):
        m.Room(name=f"Room_{i+1}", creator_id=i + 1).save(False)
    db.session.commit()

    yield client
