# -*- coding: utf-8 -*-

from flask import Blueprint, request, abort

from code.utils import make_cross_domain_response, log_any
from sentry_sdk import capture_message
from ..extensions import redis_cache, redis_user_info
from ..decorators import get_user_info
from ..utils import convert_to_int, save_token_redis
from ..constants import AppConstants
from .helper import calculate_vote, calculate_kill, is_post_allow_voter
from .tasks import add_task


rest_common = Blueprint('rest_common', __name__, url_prefix='/common')
rest_service = Blueprint('rest_service', __name__, url_prefix='/v1/voter')


@rest_service.route('/common/health_check', methods=['GET'])
def health_check():
    #capture_message('Health check route voter service')
    #health_check_task.delay()
    return make_cross_domain_response({'status': AppConstants.STATUS_OK, 'msg': 'TikTik Health Check Voter service'}, 200)


@rest_service.route('/vote_kill', methods=['POST'])
@get_user_info
def vote_kill(user_info):
    """
    Response vote click and kill click if have any change, otherwise response 0.
    """

    log_any('Call vote_kill', user_info)
    if not user_info['payload']['id']:
        return abort(401)

    if not request.json:
        return abort(400)

    post_id = request.json.get('post_id')

    # Validate post available for vote/kill
    allowed = is_post_allow_voter(post_id)

    if not allowed:
        return make_cross_domain_response(
            {'status': AppConstants.STATUS_NOT_OK, 'msg': 'This post now allow vote/kill', 'error_code': AppConstants.E_VOTE_KILL_DISABLED,
             'data': {}}, 200)

    vote = convert_to_int(request.json.get('vote'))
    kill = convert_to_int(request.json.get('kill'))

    vote = vote if vote > 0 else 0
    kill = kill if kill > 0 else 0

    num_vote, actual_vote = calculate_vote(user_info['payload']['id'], post_id, vote)
    num_kill, actual_kill = calculate_kill(user_info['payload']['id'], post_id, kill)

    if actual_vote or actual_kill:
        payload = {
            'userId': user_info['payload']['id'],
            'postId': post_id,
            'vote': actual_vote,
            'kill': actual_kill,
        }
        add_task.delay(payload)

        response = {
            'vote_click': num_vote,
            'kill_click': num_kill,
        }

        return make_cross_domain_response({'status': AppConstants.STATUS_OK, 'msg': 'success', 'error_code': AppConstants.NOT_E, 'data': response}, 200)

    # Not add vote/kill with any error.
    if not actual_vote and not actual_kill:
        return make_cross_domain_response(
            {'status': AppConstants.STATUS_NOT_OK, 'msg': 'Vote kill over', 'error_code': AppConstants.E_VOTE_KILL_OVER, 'data': {}}, 200)


@rest_service.route('/save_token', methods=['POST'])
def save_token():
    """
    Save token for testing.
    """
    token = request.json.get('token')
    if token:
        save_token_redis(token)
    return make_cross_domain_response({'status': AppConstants.STATUS_OK, 'msg': 'success', 'error_code': AppConstants.NOT_E})


@rest_service.route('/iapi/test', methods=['POST'])
def test():
    """
    Save token for testing.
    """
    return make_cross_domain_response({'status': AppConstants.STATUS_OK, 'msg': 'success', 'error_code': AppConstants.NOT_E})