# -*- coding: utf-8 -*-

from src.utils.response import make_response
from src.exceptions.base import BadRequestException
from src.constants import Constants


class ExceptionMissing(BadRequestException):
    def __init__(self, message='Missing data', errors={}, *args: object) -> None:
        super().__init__(*args)
        self.response = response = make_response(
            error_code='ERROR_INVALID_PARAMS',
            status=Constants.STATUS_NOT_OK,
            msg=message,
            errors=errors
        )

    pass
