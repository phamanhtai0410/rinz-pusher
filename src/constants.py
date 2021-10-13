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

    # Response status
    STATUS_OK = 1
    STATUS_NOT_OK = 0

    # Message
    MSG_NOT_FOUND = 'not found'
    MSG_UNKNOWN_ERROR = 'unknown error'
    MSG_SUCCESS = 'success'
    MSG_REQUIRED_AUTH = 'auth is required'

    # Error code
    CODE_NOT_E = ''
    ERROR_NOT_FOUND = 'ERROR_NOT_FOUND'
    ERROR_SERVER = 'ERROR_SERVER'
    ERROR_AUTH = 'ERROR_AUTH'
    ERROR_INVALID_PARAMS = 'ERROR_INVALID_PARAMS'
