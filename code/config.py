# -*- coding: utf-8 -*-

import os
import json
from dotenv import load_dotenv

load_dotenv()


class BaseConfig(object):
    PROJECT = "tiktik-service"

    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = False
    TESTING = False

    # http://flask.pocoo.org/docs/quickstart/#sessions
    SECRET_KEY = '\xd2\x0c\xa9\xb7\xd9E\xda-\x1e\xdb;\xb8\x0c\xfc\xbf\xf3\x16[\xa2x\xd5s\x83\xe3'


class DefaultConfig(BaseConfig):
    DEBUG = True

    # Flask-babel: http://pythonhosted.org/Flask-Babel/
    ACCEPT_LANGUAGES = ['vi']
    BABEL_DEFAULT_LOCALE = 'en'

    # Celery
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    CELERY_TASK_RESULT_EXPIRES = os.getenv('CELERY_TASK_RESULT_EXPIRES')
    CELERY_TASK_RESULT_EXPIRES = int(CELERY_TASK_RESULT_EXPIRES) if CELERY_TASK_RESULT_EXPIRES else 600
    CELERY_DEFAULT_QUEUE = 'voter_celery'
    CELERY_ROUTES = {
        'base.tasks.health_check': {'queue': 'base_health_check'},
    }
    CELERY_TRACK_STARTED = "True"

    CELERY_ENABLE_UTC = False
    CELERY_TIMEZONE = 'Asia/Ho_Chi_Minh'
    SENTRY_DSN = os.getenv('SENTRY_DSN')

    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

    REDIS_URL = os.getenv('REDIS_URL')
    REDIS_USERS_STARTUP_NODES = json.loads(os.getenv('REDIS_USERS_STARTUP_NODES'))
