# -*- coding: utf-8 -*-


class AppConstants(object):
    # Does not cache to limit below IP
    IP_WHITE_LIST = ['127.0.0.1']
    # Number of request allow one IP request in a limit time
    LIMIT_REQUEST_QUOTA = 100
    # A period time to limit one IP request, in minute
    LIMIT_REQUEST_TIME = 10
    # Interval time between two times call the same function, in second
    INTERVAL_BETWEEN_CALLS = 25
    # Telegram
    TELEGRAM_TOKEN = '1333998615:AAHnj3GzUaAdoZmBbfxl21GrrIHAfMoc6sQ'
    TELEGRAM_CHAT_ID = '-1001377339880'

    # Maximum vote, kill per post
    MAX_VOTE = 5
    MAX_KILL = 5

    # TTL Vote/Kill, 30 hours
    TTL_VOTE_KILL = 108000
    # TTL voter for a post, 30 days
    TTL_POST_VOTER = 2592000

    # Response status
    STATUS_OK = 1
    STATUS_NOT_OK = 0

    # Error code
    NOT_E = ''
    E_VOTE_KILL_OVER = 'E_VOTE_KILL_OVER'
    E_VOTE_KILL_END = 'E_VOTE_KILL_END'
    E_VOTE_KILL_DISABLED = 'E_VOTE_KILL_DISABLED'

    USER_NOT_VERIFIED_ERROR = 'USER_NOT_VERIFIED_ERROR'
    SERVER_ERROR = 'SERVER_ERROR'
    #     SUCCESS
    SUCCESS = 'SUCCESS'
    AUTH_ERROR = 'AUTH_ERROR'
    ERROR_INVALID_PARAMS = 'ERROR_INVALID_PARAMS'


_constant_response = {
    AppConstants.SUCCESS: {
        'error_code': AppConstants.NOT_E,
        'msg': 'success',
        'status': AppConstants.STATUS_OK
    },
    AppConstants.ERROR_INVALID_PARAMS: {
        'error_code': AppConstants.ERROR_INVALID_PARAMS,
        'msg': 'invalid params',
        'status': AppConstants.STATUS_NOT_OK
    },
    AppConstants.SERVER_ERROR: {
        'error_code': AppConstants.SERVER_ERROR,
        'msg': 'Invalid server',
        'status': AppConstants.STATUS_NOT_OK
    },
    AppConstants.AUTH_ERROR: {
        'error_code': AppConstants.AUTH_ERROR,
        'msg': 'Vui lòng đăng nhập để tiếp tục',
        'status': AppConstants.STATUS_NOT_OK
    },
}


def get_response_code(_code):
    """
        For get status, message, error
        @Input: Code
        @Output: {
                'error_code': '...',
                'msg': '..',
                'status': number
            }
    """
    return _constant_response.get(_code, {
        'error_code': AppConstants.NOT_E,
        'msg': 'success',
        'status': AppConstants.STATUS_OK
    })
