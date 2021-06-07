# -*- coding: utf-8 -*-
import json
from functools import wraps
from src.utils import json_encode_hook, json_decode_hook, jsonify_dict, log_any
from src.extensions import redis_cache, redis_cluster
from flask import request, abort, jsonify
from sentry_sdk import capture_exception
import jwt
import traceback

CACHE_TIMEOUT_FACTOR = 1


# timeout=1 week
def cache_id(timeout=604800, key_prefix='common', keep_timeout=False):
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
            output = redis_cluster.get(key)
            if output:
                return json.loads(output, object_hook=json_decode_hook)

            output = f(*args, **kwargs)
            # Set data to redis
            redis_cluster.setex(key, timeout, json.dumps(output, default=json_encode_hook))
            return output

        return wrapper

    return decorator


# timeout = 1 day
def cache_filter(timeout=86400, key_prefix='common', key_fields=[], keep_timeout=False):
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
            _filter = dict()
            for key_field in key_fields:
                _filter[key_field] = kwargs.get(key_field)
            key = "%s:%s" % (key_prefix, jsonify_dict(_filter))
            output = redis_cluster.get(key)
            if output:
                return json.loads(output, object_hook=json_decode_hook)

            output = f(*args, **kwargs)
            # Set data to redis
            redis_cluster.setex(key, timeout, json.dumps(output, default=json_encode_hook))
            return output

        return wrapper

    return decorator


def get_user_info(f):
    """
        Decorator to check and get user info from user token. Return
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        if not request:  # Outside flask app context
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
        token_existed = redis_cluster.get(rq_user_token)
        # TODO below line for testing
        # redis_user_info.setex(rq_user_token, 15000, 1)

        user_info = None
        if token_existed:  # In case user info exists, decode it
            try:
                user_info = jwt.decode(rq_user_token, algorithm="RS256", options={"verify_signature": False})
            except:
                traceback.print_exc()
                capture_exception()
        # TODO check here
        # if not user_info:
        #     return jsonify({
        #         'status': 0,
        #         'error_code': 'ERROR_BASE_REQUIRE_LOGIN',
        #         'msg': 'login to continue',
        #         'data': {}
        #     }), 401
        if not user_info:
            user_info = {
                "payload": {
                    "id": None,
                }
            }
        decorated_kwargs = {**kwargs, 'user_info': user_info.get('payload', {})}
        return f(*args, **decorated_kwargs)

    return wrapper
