import json
import traceback

from sentry_sdk import capture_exception

from src.utils.format import json_encode_hook


def logger(x, *args, **kwargs):
    '''
    Log any message to json format.
    '''
    try:
        msg = {
            'msg': x,
        }
        print()
        if args:
            msg['args'] = json.dumps(args, default=json_encode_hook)
        if kwargs:
            msg['kwargs'] = json.dumps(args, default=json_encode_hook)
        print(msg)
    except:
        capture_exception()
        traceback.print_exc()
