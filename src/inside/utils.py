import json
import traceback

import requests
import sentry_sdk

from src.config import DefaultConfig


def use_request_inside(url, method, body={}, params={}):
    try:
        headers = {
            'Content-Type': 'application/json',
            'apiKey': DefaultConfig.INSIDE_APIKEY
        }
        _data = json.dumps(body)
        response = requests.request(method=method,
                                    url=url,
                                    data=_data,
                                    params=params,
                                    headers=headers,
                                    timeout=6)
        if response:
            return response.json()
    except:
        sentry_sdk.capture_exception()
        traceback.print_exc()
    return None
