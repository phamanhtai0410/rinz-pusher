# -*- coding: utf-8 -*-

import os
import traceback

import sentry_sdk
from sentry_sdk import capture_exception, capture_message
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask, request, jsonify
from flask_babel import Babel
from .common import rest_service
from .config import DefaultConfig
from .extensions import redis_cache, db, jobs
from jsonschema import ValidationError
from .sms import rest_sms

# For import *
__all__ = ['create_app']

from .shedule import get_token_for_fpt_sms

DEFAULT_BLUEPRINTS = (
    rest_service,
    rest_sms,
)


def create_app(config=None, app_name=None, blueprints=None):
    """Create a Flask app."""

    if app_name is None:
        app_name = DefaultConfig.PROJECT
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(app_name, instance_relative_config=True)
    configure_app(app, config)
    configure_hook(app)
    configure_blueprints(app, blueprints)
    configure_extensions(app)
    configure_template_filters(app)
    configure_error_handlers(app)
    configure_logging_level()
    configure_jobs(app)
    return app


def configure_jobs(app):
    get_token_for_fpt_sms()
    jobs.add_job(
        get_token_for_fpt_sms,
        trigger='interval',
        # minute=1,
        hour=1
    )
    jobs.start()


def configure_app(app, config=None):
    """Different ways of configurations."""

    # http://flask.pocoo.org/docs/api/#configuration
    app.config.from_object(DefaultConfig)

    # http://flask.pocoo.org/docs/config/#instance-folders
    app.config.from_pyfile('production.cfg', silent=True)

    if config:
        app.config.from_object(config)


def configure_extensions(app):
    # flask-sqlalchemy
    db.init_app(app)
    print('Connect with Mysql successfully')

    # Redis
    redis_cache.init_app(app)
    print('Init Redis cache successfully')
    # redis_user_info.init_app(app, config_prefix='REDIS_USERS')
    # print('Init Redis user info successfully')

    # Flask Babel
    babel = Babel(app)

    # Sentry
    if DefaultConfig.SENTRY_DSN:
        sentry_sdk.init(
            dsn=DefaultConfig.SENTRY_DSN,
            integrations=[FlaskIntegration()],
            server_name=DefaultConfig.PROJECT
        )

        capture_message('{} starts'.format(DefaultConfig.PROJECT))

    @babel.localeselector
    def get_locale():
        accept_languages = app.config.get('ACCEPT_LANGUAGES')
        return request.accept_languages.best_match(accept_languages)


def configure_blueprints(app, blueprints):
    """Configure blueprints in views."""

    for blueprint in blueprints:
        app.register_blueprint(blueprint, url_prefix="{}/{}".format("/v1/3th", blueprint.url_prefix))


def configure_template_filters(app):
    @app.template_filter()
    def pretty_date(value):
        return pretty_date(value)

    @app.template_filter()
    def format_date(value, format='%Y-%m-%d'):
        return value.strftime(format)


def configure_logging_level():
    import logging
    logging.getLogger('suds').setLevel(logging.ERROR)


def configure_hook(app):
    @app.before_request
    def before_request():
        pass


def configure_error_handlers(app):
    @app.errorhandler(403)
    def forbidden_page(error):
        return jsonify({
            'status': 0,
            'error_code': 'ERROR_METADATA_FORBIDDEN',
            'msg': 'forbidden',
            'data': {}
        }), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            'status': 0,
            'error_code': 'ERROR_METADATA_NOT_FOUND',
            'msg': 'notfound',
            'data': {}
        }), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return jsonify({
            'status': 0,
            'error_code': 'ERROR_METADATA_SERVER_ERROR',
            'msg': 'server error',
            'data': {}
        }), 500

    @app.errorhandler(400)
    def bad_request(error):
        if isinstance(error.description, ValidationError):
            original_error = error.description
            return jsonify({
                'status': 0,
                'error_code': 'ERROR_METADATA_VALIDATION',
                'msg': original_error.message,
                'data': {}
            }), 400
        return error
