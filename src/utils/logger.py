import json
import traceback
from datetime import datetime

from sentry_sdk import capture_exception

from src.utils.format import json_encode_hook


class Bcolors():
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Logger(object):
    '''
    Log any message to json format.
    [TYPE] - %H:%M:%S.%f %d-%m-%Y - info
    '''

    @staticmethod
    def debug(x, *args, **kwargs):
        try:

            msg = {
                'msg': x,
            }
            print('')
            if args:
                msg['args'] = json.dumps(args, default=json_encode_hook)
            if kwargs:
                msg['kwargs'] = json.dumps(args, default=json_encode_hook)
            msg = json.dumps(msg, default=json_encode_hook)
            print(f'{Bcolors.OKGREEN}[DEBUG] - {datetime.utcnow().strftime("%H:%M:%S.%f %d-%m-%Y")} {Bcolors.ENDC}')
            print(f'{Bcolors.OKCYAN}          {msg} {Bcolors.ENDC}')
        except:
            capture_exception()
            traceback.print_exc()

    @staticmethod
    def error(x, *args, **kwargs):
        try:
            msg = {
                'msg': x,
            }
            print('')
            if args:
                msg['args'] = json.dumps(args, default=json_encode_hook)
            if kwargs:
                msg['kwargs'] = json.dumps(args, default=json_encode_hook)
            msg = json.dumps(msg, default=json_encode_hook)
            print(f'{Bcolors.FAIL}[ERROR] - {datetime.utcnow().strftime("%H:%M:%S.%f %d-%m-%Y")} {Bcolors.ENDC}')
            print(f'{Bcolors.OKCYAN}          {msg} {Bcolors.ENDC}')
        except:
            capture_exception()
            traceback.print_exc()
