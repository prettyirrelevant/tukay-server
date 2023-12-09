import logging

from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler

from .responses import error_response

logger = logging.getLogger(__name__)


def custom_exception_handler(exception, context) -> Response | None:
    if not isinstance(exception, serializers.ValidationError):
        logger.exception(
            'An exception occurred while handling request %s',
            context['request'].get_full_path(),
            exc_info=exception,
        )

    response = exception_handler(exception, context)
    if response is None:
        return None

    if isinstance(exception, APIException):
        return error_response(
            message=exception.__class__.__name__,
            errors=[exception.detail] if isinstance(exception.detail, str) else exception.detail,
            status_code=response.status_code,
        )

    return error_response(message=str(exception), errors=None, status_code=response.status_code)
