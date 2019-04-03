from sqlalchemy_utils import database_exists, create_database, drop_database

from app.libs.models import *


def create_db():
    """
    Setup a new DB.
    """
    from flask import Flask
    import configparser
    import os

    app = Flask(__name__)
    config = configparser.ConfigParser()
    config.read(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "../config.ini")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = config["DATABASE"]["CONNECTION_STRING"]
    db.init_app(app)
    with app.app_context():
        if not database_exists(config["DATABASE"]["CONNECTION_STRING"]):
            create_database(config["DATABASE"]["CONNECTION_STRING"])
        db.create_all()

        g.user = 1
        db_data()


def reset_db():
    """
    Reset the DB
    """
    import configparser
    import os

    config = configparser.ConfigParser()
    config.read(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "../config.ini")
    )
    if database_exists(config["DATABASE"]["CONNECTION_STRING"]):
        db.drop_all()
    create_db()


def db_data():
    """
    Fake data for testing.
    """
    pass