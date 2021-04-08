# -*- coding: utf-8 -*-

import traceback
from enum import Enum, auto


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
    TTL_VOTE_KILL =  108000
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
