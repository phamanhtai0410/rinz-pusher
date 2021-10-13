# -*- coding: utf-8 -*-
import os

from flask_redis import Redis
from apscheduler.schedulers.background import BackgroundScheduler
import firebase_admin

# Redis cache
from rediscluster import RedisCluster

from src.config import DefaultConfig

redis_cache = Redis()

# Redis user info, will initialized in app
redis_cluster = RedisCluster(startup_nodes=DefaultConfig.REDIS_CLUSTER,
                             decode_responses=True)

redis_global = RedisCluster(startup_nodes=DefaultConfig.REDIS_GLOBAL,
                            decode_responses=True)

firebase_credentials = firebase_admin.credentials.Certificate(os.getcwd() + "/keys/firebase.json")

# db = SQLAlchemy()
jobs = BackgroundScheduler(daemon=True)
