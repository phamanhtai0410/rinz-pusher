import traceback

import sentry_sdk

from src.utils.logger import logger


def name_job():
    try:
        logger('____________ some_thing __________')

    except:
        sentry_sdk.capture_exception()
        traceback.print_exc()
