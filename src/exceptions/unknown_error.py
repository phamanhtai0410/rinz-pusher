# -*- coding: utf-8 -*-

from src.utils.response import make_response
from src.exceptions.base import BadRequestException
from src.constants import Constants


class ExceptionUnknownError(BadRequestException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.response = make_response(
            status=Constants.STATUS_NOT_OK,
            msg=Constants.MSG_UNKNOWN_ERROR,
            error_code=Constants.ERROR_SERVER
        )

    pass
