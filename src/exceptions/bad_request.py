# -*- coding: utf-8 -*-

from src.utils.response import make_response
from src.exceptions.base import BadRequestException
from src.constants import Constants


class ExceptionBadRequest(BadRequestException):
    def __init__(self, message='Bad request', *args: object) -> None:
        super().__init__(*args)
        self.response = make_response(
            error_code='ERROR_BAD_REQUEST',
            status=Constants.STATUS_NOT_OK,
            msg=message
        )
    pass
