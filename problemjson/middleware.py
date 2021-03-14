# -*- coding: utf-8 -*-

# Django
from django.http import JsonResponse

# Project
from .exception import APIException


class HTTPProblemJSONMiddleware:
    """Support RFC-7807 'HTTP Problem' exception handling."""

    def __init__(self, get_response):
        """One-time configuration and initialisation."""
        self.get_response = get_response
        self.content_type = 'application/problem+json'

    def __call__(self, request):
        """Process request."""
        return self.get_response(request)

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
