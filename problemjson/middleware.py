# -*- coding: utf-8 -*-

# Django
import logging
from functools import wraps

from django.http import JsonResponse

# Local
from .exceptions import APIException, BadRequest, Forbidden, NotFound

CONTENT_TYPE = 'application/problem+json'

def _process_exception(request, exception):
    if not isinstance(exception, APIException):
        exception = APIException()
    data = {
        'title': exception.title,
        'status': exception.status_code,
        'instance': request.get_full_path(),
        }
    status_code = int(exception.status_code)
    response = JsonResponse(
        data,
        content_type=CONTENT_TYPE,
        status=status_code,
        )
    return response


def capture_exception(func):
    """Decorate process_exception with exception capturing."""
    @wraps(func)
    def wrapper(self, request, exception):
        logging.exception(exception)
        return func(self, request, exception)

    return wrapper


class HTTPProblemJSONMiddleware:
    """Support RFC-7807 'HTTP Problem' exception handling."""

    def __init__(self, get_response):
        """One-time configuration and initialisation."""
        self.get_response = get_response
        self.content_type = CONTENT_TYPE

    def __call__(self, request):
        """Process request."""
        return self.get_response(request)

    @capture_exception
    def process_exception(self, request, exception):
        if not isinstance(exception, APIException):
            exception = APIException()
        data = {
            'title': exception.title,
            'status': exception.status_code,
            'instance': request.get_full_path(),
            }
        status_code = exception.status_code

        return JsonResponse(
            data,
            content_type=self.content_type,
            status=status_code,
            )


def handler400(request, exception):
    return _process_exception(request, BadRequest())


def handler403(request, exception):
    return _process_exception(request, Forbidden())


def handler404(request, exception):
    return _process_exception(request, NotFound())


def handler500(request, exception):
    return _process_exception(request, APIException())
