# -*- coding: utf-8 -*-

from ..extensions import redis_cache
from ..constants import AppConstants
from ..utils import get_redis_cache
from .models import Voter

def get_vote_kill(user_id, post_id):
    """
    Get user vote/kill on specific post
    :param user_id:
    :param post_id:
    :return: _vote, _kill
    """
    voting = Voter.get_voter(user_id, post_id)
    _vote = 0
    _kill = 0
    for i in voting:
        _vote += i.vote
        _kill += i.kill

    return _vote, _kill

def calculate_vote(user_id, post_id, vote):
    """
    Calculate number of vote
    """

    if vote <= 0:
        return 0, 0

    key = 'vote:%s:%s' % (user_id, post_id)

    if redis_cache.exists(key):
        exist_vote = redis_cache.get(key)
    else:
        exist_vote, exist_kill = get_vote_kill(user_id, post_id)

    exist_vote = 0 if not exist_vote else int(exist_vote)
    vote += exist_vote
    num_vote = AppConstants.MAX_VOTE if vote > AppConstants.MAX_VOTE else vote

    redis_cache.setex(key, AppConstants.TTL_VOTE_KILL, num_vote)

    return num_vote, num_vote - exist_vote


def calculate_kill(user_id, post_id, kill):
    """
    Calculate number of kill
    """

    if kill <= 0:
        return 0, 0

    key = 'kill:%s:%s' % (user_id, post_id)

    if redis_cache.exists(key):
        exist_kill = redis_cache.get(key)
    else:
        exist_vote, exist_kill = get_vote_kill(user_id, post_id)

    exist_kill = 0 if not exist_kill else int(exist_kill)
    kill += exist_kill
    num_kill = AppConstants.MAX_KILL if kill > AppConstants.MAX_KILL else kill

    redis_cache.setex(key, AppConstants.TTL_VOTE_KILL, num_kill)

    return num_kill, num_kill - exist_kill


def is_post_allow_voter(post_id):
    """
    Check if post allow vote/kill or not
    :param post_id:
    :return: True if allowed, otherwise False.
    """

    key = 'be:feeds:id:%s' % (post_id)
    post_data = get_redis_cache(key)
    # TODO check post public or not
    #if post_data and 'deciding' in post_data and 'show' == post_data['status']:
    if post_data and 'deciding' in post_data:
        # Check enable voter
        return post_data['deciding']

    # TODO remove for prod
    return True


def calculate_post_vote(post_id, vote):
    """
    Calculate number of vote.
    """

    if vote <= 0:
        return 0, 0

    key = 'vote:%s' % post_id

    if redis_cache.exists(key):
        exist_vote = redis_cache.get(key)
    else:
        # TODO check DB, total vote for this post
        exist_vote = 0

    exist_vote = 0 if not exist_vote else int(exist_vote)
    vote += exist_vote

    redis_cache.setex(key, AppConstants.TTL_POST_VOTER, vote)

    return vote


def calculate_post_kill(post_id, kill):
    """
    Calculate number of kill.
    """

    if kill <= 0:
        return 0, 0

    key = 'kill:%s' % post_id

    if redis_cache.exists(key):
        exist_kill = redis_cache.get(key)
    else:
        # TODO check DB, total kill for this post
        exist_kill = 0

    exist_kill = 0 if not exist_kill else int(exist_kill)
    kill += exist_kill

    redis_cache.setex(key, AppConstants.TTL_POST_VOTER, kill)

    return kill
