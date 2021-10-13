# -*- coding: utf-8 -*-
import traceback

import firebase_admin
import sentry_sdk
from celery import Celery
from flask import Flask
from pymodm import connect
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk import capture_message, capture_exception

from .config import DefaultConfig
from .extensions import redis_cache, firebase_credentials
from .utils.logger import Logger


def create_app(config=None, app_name=None, blueprints=None):
    """Create a Flask app."""

    if app_name is None:
        app_name = DefaultConfig.PROJECT

    app = Flask(app_name, instance_relative_config=True)
    configure_app(app, config)
    configure_extensions(app)

    return app


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
    # db.init_app(app)
    Logger.debug('Connect with Mysql successfully')
    try:
        firebase_admin.initialize_app(firebase_credentials)
        Logger.debug('Init firebase admin done')
    except:
        capture_exception()
        traceback.print_exc()

    connect(DefaultConfig.MONGODB_URI, connect=False)

    print('Connect with MongoDB successfully')

    # Redis
    redis_cache.init_app(app)

    Logger.debug('Init Redis cache successfully')

    # Sentry
    if DefaultConfig.SENTRY_DSN:
        sentry_sdk.init(
            dsn=DefaultConfig.SENTRY_DSN,
            integrations=[FlaskIntegration()],
            debug=True,
            server_name=DefaultConfig.PROJECT
        )

        capture_message('{} celery starts'.format(DefaultConfig.PROJECT))


def create_celery_app(app=None):
    app = app or create_app()
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    Logger.debug('Init Celery tasks app')

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = create_celery_app()
