import traceback

import sentry_sdk

from src.utils import log_any


def name_job():
    try:
        log_any('____________ some_thing __________')

    except Exception as e:
        sentry_sdk.capture_exception(e)
        traceback.print_exception(e)
