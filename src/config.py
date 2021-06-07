# -*- coding: utf-8 -*-

import os
import json
from dotenv import load_dotenv

load_dotenv()


class BaseConfig(object):
    PROJECT = "the-cua-tui-3th"

    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = False
    TESTING = False

    # http://flask.pocoo.org/docs/quickstart/#sessions
    SECRET_KEY = '\xd2\x0c\xa9\xb7\xd9E\xda-\x1e\xdb;\xb8\x0c\xfc\xbf\xf3\x16[\xa2x\xd5s\x83\xe3'


class DefaultConfig(BaseConfig):
    DEBUG = True
    PREFIX = '/v1/template'
    # Flask-babel: http://pythonhosted.org/Flask-Babel/
    ACCEPT_LANGUAGES = ['vi']
    BABEL_DEFAULT_LOCALE = 'en'

    # Celery
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    CELERY_TASK_RESULT_EXPIRES = os.getenv('CELERY_TASK_RESULT_EXPIRES')
    CELERY_TASK_RESULT_EXPIRES = int(CELERY_TASK_RESULT_EXPIRES) if CELERY_TASK_RESULT_EXPIRES else 600
    CELERY_DEFAULT_QUEUE = 'the-cua-tui-3th'
    CELERY_ROUTES = {
        'base.tasks.health_check': {'queue': 'the-cua-tui-3th'},
        'connect_3th_send_sms': {'queue': 'the-cua-tui-3th'}
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

    FPT_CLIENT_ID_CMS = os.getenv('FPT_CLIENT_ID_CMS')
    FPT_CLIENT_SECRET_CMS = os.getenv('FPT_CLIENT_SECRET_CMS')
    FPT_URL_CMS = os.getenv('FPT_URL_CMS')
