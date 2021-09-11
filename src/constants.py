# -*- coding: utf-8 -*-


class Constants(object):
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
    # Message
    MSG_REQUIRED_AUTH = 'Vui lòng đăng nhập để tiếp tục'
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
    SUCCESS = 'SUCCESS'
    AUTH_ERROR = 'AUTH_ERROR'
    ERROR_INVALID_PARAMS = 'ERROR_INVALID_PARAMS'


_constant_response = {
    Constants.SUCCESS: {
        'error_code': Constants.NOT_E,
        'msg': 'success',
        'status': Constants.STATUS_OK
    },
    Constants.ERROR_INVALID_PARAMS: {
        'error_code': Constants.ERROR_INVALID_PARAMS,
        'msg': 'invalid params',
        'status': Constants.STATUS_NOT_OK
    },
    Constants.SERVER_ERROR: {
        'error_code': Constants.SERVER_ERROR,
        'msg': 'Invalid server',
        'status': Constants.STATUS_NOT_OK
    },
    Constants.AUTH_ERROR: {
        'error_code': Constants.AUTH_ERROR,
        'msg': 'Vui lòng đăng nhập để tiếp tục',
        'status': Constants.STATUS_NOT_OK
    },
}
