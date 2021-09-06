# -*- coding: utf-8 -*-

from src.utils import make_cross_domain_response, log_any


def cl_health_check():
    log_any("call health_check")
    payload = {
        "info": "log health_check"
    }
    return make_cross_domain_response()
