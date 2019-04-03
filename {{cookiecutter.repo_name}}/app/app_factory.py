from flask_wtf.csrf import CSRFError
from flask import Flask, render_template, request
from app.database import db
import configparser
import os
from flask import got_request_exception
import logging
from app.extensions import csrf, login_manager, migrate
from flask import g
from flask_login import current_user


def create_app(config_path, settings_override=None):
    """
    Create a new app.
    :param config_path:
    :type config_path:
    :param settings_override:
    :type settings_override:
    :return:
    :rtype:
    """
    app = Flask(__name__)
    config = configparser.ConfigParser()
    config.read(config_path)
    # app.config['SERVER_NAME'] = 'localhost'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = config["DATABASE"]["CONNECTION_STRING"]
    app.config["ENVIRONMENT"] = config["ENV"]["STAGE"]

    app.debug = True if config["ENV"]["STAGE"] == "dev" else False
    app.secret_key = config["ENV"]["SECRET_KEY"]
    app.security_password_salt = config["ENV"]["SECURITY_PASSWORD_SALT"]
    app.config["WTF_CSRF_TIME_LIMIT"] = 86400

    if settings_override:
        app.config.update(settings_override)
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "core.login"

    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    @app.errorhandler(CSRFError)
    def handle_csrf_error(error):
        app.logger.error(error)
        return (
            render_template("errors/csrfErrorPage.html", reason=error.description),
            400,
        )

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(error)
        return render_template("errors/500.html", reason=error.description), 500

    @app.errorhandler(404)
    def not_found(error):
        app.logger.error(error)
        app.logger.error(request)
        app.logger.error(request.url_rule)
        return render_template("errors/404.html", reason=error.description), 404

    return app
