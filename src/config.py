# -*- coding: utf-8 -*-

import os
import json
from dotenv import load_dotenv

load_dotenv()


class BaseConfig(object):
    PROJECT = "service"

    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = False
    TESTING = False

    # http://flask.pocoo.org/docs/quickstart/#sessions
    SECRET_KEY = '\xd2\x0c\xa9\xb7\xd9E\xda-\x1e\xdb;\xb8\x0c\xfc\xbf\xf3\x16[\xa2x\xd5s\x83\xe3'


class DefaultConfig(BaseConfig):
    DEBUG = True
    PREFIX = '/v1/push'
    # Flask-babel: http://pythonhosted.org/Flask-Babel/
    ACCEPT_LANGUAGES = ['vi']
    BABEL_DEFAULT_LOCALE = 'en'

    # Celery
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    CELERY_TASK_RESULT_EXPIRES = os.getenv('CELERY_TASK_RESULT_EXPIRES')
    CELERY_TASK_RESULT_EXPIRES = int(CELERY_TASK_RESULT_EXPIRES) if CELERY_TASK_RESULT_EXPIRES else 600
    CELERY_DEFAULT_QUEUE = 'service-push-queue'
    CELERY_ROUTES = {
        'push.tasks.remove_device': {'queue': 'service-push-queue'},
        'push.tasks.firebase.subscribe': {'queue': 'service-push-queue'},
        'push.tasks.firebase.unsubscribe': {'queue': 'service-push-queue'},
        'push.tasks.firebase.send_topic_use_condition': {'queue': 'service-push-queue'},
        'push.tasks.user.insert_notification': {'queue': 'service-push-queue'},
        'push.tasks.user.mark_notification_task': {'queue': 'service-push-queue'},
        'template': {'queue': 'service-push-queue'}
    }
    CELERY_TRACK_STARTED = "True"

    CELERY_ENABLE_UTC = False
    CELERY_TIMEZONE = 'Asia/Ho_Chi_Minh'
    SENTRY_DSN = os.getenv('SENTRY_DSN')

    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

    # Redis for local service
    REDIS_URL = os.getenv('REDIS_URL')

    # Redis cluster for all service in RinZ: Ex: music, farm, network, .v.v.
    REDIS_GLOBAL = json.loads(os.getenv('REDIS_GLOBAL', default='[]'))

    # Redis cluster for group service
    REDIS_CLUSTER = json.loads(os.getenv('REDIS_CLUSTER', default='[]'))

    MONGODB_URI = os.getenv('MONGODB_GLOBAL')

    CACHE_SUB = ''
    INSIDE_APIKEY = os.getenv('INSIDE_APIKEY')
    CACHING = os.getenv('CACHING', False)
