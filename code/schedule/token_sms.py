import json
import traceback
import uuid

import requests
import sentry_sdk

from code.config import DefaultConfig
from code.extensions import redis_cluster


def get_token_for_fpt_sms():
    try:
        print('____________ start run jobs __________')
        session_id = str(uuid.uuid4())
        payload = {
            "grant_type": "client_credentials",
            "client_id": DefaultConfig.FPT_CLIENT_ID_CMS,
            "client_secret": DefaultConfig.FPT_CLIENT_SECRET_CMS,
            "scope": "send_brandname_otp",
            "session_id": session_id
        }
        data = json.dumps(payload)
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", 'https://app.sms.fpt.net/oauth2/token',
                                    data=data,
                                    headers=headers,
                                    timeout=20,
                                    verify=False)
        print('response.text', response.json())
        response_data = response.json()

        print(response.text)
        if response_data:
            # response_data = response.json()
            access_token = response_data.get('access_token')
            if access_token:
                redis_data = {
                    'session_id': session_id,
                    'access_token': access_token
                }
                dum_data = json.dumps(redis_data)
                print('data: {}'.format(dum_data))
                redis_cluster.set('3th:fpt:sms', dum_data)
        print('_______________________ done ______________________')

    except Exception as e:
        sentry_sdk.capture_exception(e)
        traceback.print_exception(e)

