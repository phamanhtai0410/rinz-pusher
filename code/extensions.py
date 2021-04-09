# -*- coding: utf-8 -*-
from flask_redis import Redis

from rediscluster import RedisCluster
from .config import DefaultConfig

# Redis cache
redis_cache = Redis()
# Redis user info, will initialized in app
redis_cluster = RedisCluster(startup_nodes=DefaultConfig.REDIS_USERS_STARTUP_NODES,
                             decode_responses=True)  # print('Init Redis user info successfully')
# redis_user_info=None

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
