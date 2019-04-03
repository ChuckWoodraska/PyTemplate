import os

import pytest
from flask import g
from app.app_factory import create_app
from app.database import db as _db
from app.libs.models import *
from app.libs.utils import db_data


@pytest.yield_fixture(scope="session")
def app():
    """Session-wide test `Flask` application."""
    settings_override = {
        "SERVER_NAME": "localhost",
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
    }
    config_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "test_config.ini"
    )
    app_instance = create_app(config_path, settings_override)

    # Establish an application context before running the tests.
    ctx = app_instance.app_context()
    ctx.push()

    yield app_instance

    ctx.pop()


@pytest.yield_fixture()
def client(app):
    """
    Setup an app client, this gets executed for each test function.

    :param app: Pytest fixture
    :return: Flask app client
    """
    yield app.test_client()


@pytest.yield_fixture(scope="session")
def db(app):
    """Session-wide test database."""

    _db.app = app
    _db.drop_all()
    _db.create_all()

    with app.app_context():
        g.user = 1
        db_data()

        _db.session.commit()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.yield_fixture()
def session(db):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    scoped_session = db.create_scoped_session(options=options)

    db.session = scoped_session

    yield db.session

    transaction.rollback()
    connection.close()
    scoped_session.remove()
    db.session.close_all()
