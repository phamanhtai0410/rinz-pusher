# -*- coding: utf-8 -*-
from functools import wraps
from code.utils import json_encode_hook, json_decode_hook, jsonify_dict, log_any
from code.extensions import redis_cache, redis_user_info
from flask import request, abort
from sentry_sdk import capture_exception
import msgpack
import jwt
import traceback



CACHE_TIMEOUT_FACTOR = 1


def cache_id(timeout=100, key_prefix='common', keep_timeout=False):
    """
    Decorator for caching functions by id, using its arguments as part of the key.
    Returns the cached value, or the function if the cache is disabled
    """
    if timeout is None:
        timeout = 300

    if not keep_timeout:
        timeout *= CACHE_TIMEOUT_FACTOR

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            key = "%s:id:%s" % (key_prefix, args[0])
            output = redis_cache.get(key)
            if output:
                return msgpack.loads(output, object_hook=json_decode_hook)

            output = f(*args, **kwargs)
            # Set data to redis
            redis_cache.setex(key, timeout, msgpack.dumps(output, default=json_encode_hook))
            return output

        return wrapper

    return decorator


def cache_filter(timeout=100, key_prefix='common', filter={}, keep_timeout=False):
    """
    Decorator for caching functions by filter
    Returns the cached value, or the function if the cache is disabled
    """
    if timeout is None:
        timeout = 300

    if not keep_timeout:
        timeout *= CACHE_TIMEOUT_FACTOR

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            key = "%s:%s" % (key_prefix, jsonify_dict(filter))
            output = redis_cache.get(key)
            if output:
                return msgpack.loads(output, object_hook=json_decode_hook)

            output = f(*args, **kwargs)
            # Set data to redis
            redis_cache.setex(key, timeout, msgpack.dumps(output, default=json_encode_hook))
            return output

        return wrapper

    return decorator


def get_user_info(f):
    """
        Decorator to check and get user info from user token. Return
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not request:     # Outside flask app context
            return f(user_info=None, *args, **kwargs)

        rq_user_token = request.headers.get('Authorization')
        if not rq_user_token or 'Bearer ' not in rq_user_token:
            user_info = {
                "payload": {
                    "id": None,
                }
            }

            return f(user_info=user_info, *args, **kwargs)

        rq_user_token = rq_user_token.split(' ')[1]
        # Get user token on Redis user info
        token_existed = redis_user_info.get(rq_user_token)
        # TODO below line for testing
        #redis_user_info.setex(rq_user_token, 15000, 1)

        user_info = None
        if token_existed:  # In case user info exists, decode it
            try:
                user_info = jwt.decode(rq_user_token, algorithm="RS256", options={"verify_signature": False})
            except:
                traceback.print_exc()
                capture_exception()

        if not user_info:
            user_info = {
                "payload": {
                    "id": None,
                }
            }

        return f(user_info=user_info, *args, **kwargs)

    return wrapper
