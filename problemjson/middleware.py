# -*- coding: utf-8 -*-

# Django
import logging
from functools import wraps

from django.http import JsonResponse

# Local
from .exceptions import APIException


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
        self.content_type = 'application/problem+json'

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
