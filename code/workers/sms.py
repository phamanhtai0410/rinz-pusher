import base64
import json
import traceback

import requests
from sentry_sdk import capture_exception

from code.extensions import redis_cluster
from code.modles.hooklog import HookLog
from code.modles.verifycode import VerifyCode
from code.tasks import celery


def get_config_fpt():
    try:
        cong = redis_cluster.get('3th:fpt:sms')
        if cong:
            return json.loads(cong)
        return {}
    except Exception as e:
        capture_exception(e)
        traceback.print_exception(e)
    return {}


@celery.task(name='connect_3th_send_sms', rate_limit='100/s')
def send_phone_task(phone, code, user_id):
    try:
        try:
            VerifyCode.add({
                'user_id': user_id,
                'code_number': code,
                'phone_number': phone
            })
        except Exception as e:
            capture_exception(e)
        # data = {
        #     "ApiKey": DefaultConfig.SMS_ApiKey,
        #     "Content": "{} la ma xac minh dang ky {} cua ban".format(code, DefaultConfig.SMS_Brandname),
        #     "Phone": phone,
        #     "SecretKey": DefaultConfig.SMS_SecretKey,
        #     "IsUnicode": False,
        #     "SmsType": DefaultConfig.SMS_SmsType,
        #     "Brandname": DefaultConfig.SMS_Brandname
        # }
        data_config = get_config_fpt()
        message = "Ma OTP Thecuatui cua ban la {}. Ma co hieu luc trong vong 10 phut. Xin khong chia se ma cho bat ky ai. YourConnect xin cam on!".format(
            code)
        sample_string_bytes = message.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        base64_string = base64_bytes.decode("ascii")
        data = {
            **data_config,
            "BrandName": "YourConnect",
            "Phone": phone,
            "Message": base64_string
        }
        payload = json.dumps(data)
        headers = {
            'Content-Type': 'application/json'
        }
        print(data)
        url = "https://app.sms.fpt.net/api/push-brandname-otp"  # DefaultConfig.SMS_URL
        # response = requests.request("POST", url,
        #                             data=payload,
        #                             headers=headers,
        #                             verify=False)
        # print('response.text', response.text)
        # HookLog.add({
        #     'from_service': 'id',
        #     'to_service': 'sms_fpt',
        #     'data': data,
        #     'response': response.text,
        #     'headers': headers,
        #     'url': url
        # })
    except Exception as e:
        capture_exception(e)
        traceback.print_exception(e)
    return "send_code done"
