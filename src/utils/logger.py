import json
import traceback
from datetime import datetime

from sentry_sdk import capture_exception

from src.utils.format import json_encode_hook
from inspect import getframeinfo, stack


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
            caller = getframeinfo(stack()[1][0])
            msg = {
                'msg': x,
            }
            args_and_kwargs = {}
            print('')
            if args:
                args_and_kwargs['args'] = json.dumps(args, default=json_encode_hook)
            if kwargs:
                args_and_kwargs['kwargs'] = json.dumps(args, default=json_encode_hook)
            msg = json.dumps(msg, default=json_encode_hook)
            print(f'{Bcolors.OKGREEN}[DEBUG] - {datetime.utcnow().strftime("%H:%M:%S.%f %d-%m-%Y")} {Bcolors.ENDC}')
            print(f'{Bcolors.BOLD} {caller.filename} : {caller.lineno} {Bcolors.ENDC}')
            print(f'{Bcolors.OKCYAN}          {msg} {Bcolors.ENDC}')
            if args_and_kwargs:
                print(f'{Bcolors.WARNING}          {args_and_kwargs} {Bcolors.ENDC}')

        except:
            capture_exception()
            traceback.print_exc()

    @staticmethod
    def error(x, *args, **kwargs):
        try:
            caller = getframeinfo(stack()[1][0])
            msg = {
                'msg': x,
            }
            print('')
            args_and_kwargs = {}
            if args:
                args_and_kwargs['args'] = json.dumps(args, default=json_encode_hook)
            if kwargs:
                args_and_kwargs['kwargs'] = json.dumps(args, default=json_encode_hook)
            msg = json.dumps(msg, default=json_encode_hook)
            print(f'{Bcolors.FAIL}[ERROR] - {datetime.utcnow().strftime("%H:%M:%S.%f %d-%m-%Y")} {Bcolors.ENDC}')
            print(f'{Bcolors.BOLD} {caller.filename} : {caller.lineno} {Bcolors.ENDC}')
            print(f'{Bcolors.OKCYAN}          {msg} {Bcolors.ENDC}')
            if args_and_kwargs:
                print(f'{Bcolors.WARNING}          {args_and_kwargs} {Bcolors.ENDC}')
        except:
            capture_exception()
            traceback.print_exc()
