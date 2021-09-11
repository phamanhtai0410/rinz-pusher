import traceback

import sentry_sdk

from src.utils.logger import Logger


def name_job():
    try:
        Logger.debug('____________ some_thing __________')

    except:
        sentry_sdk.capture_exception()
        traceback.print_exc()
