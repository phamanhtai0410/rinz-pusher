# -*- coding: utf-8 -*-
from flask_redis import Redis
from apscheduler.schedulers.background import BackgroundScheduler
from flask_sqlalchemy import SQLAlchemy

# Redis cache
redis_cache = Redis()
# Redis user info, will initialized in app
redis_cluster = None # RedisCluster(startup_nodes=DefaultConfig.REDIS_USERS_STARTUP_NODES,
                    #         decode_responses=True)

db = SQLAlchemy()
jobs = BackgroundScheduler(daemon=True)
