# -*- coding: utf-8 -*-

# Standard Library
from http import HTTPStatus as status

# Django
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _


class APIException(Exception):
    """Base class for API exceptions.

    Subclasses should provide `.status_code` and `.default_detail` properties.
    """

    status_code = status.INTERNAL_SERVER_ERROR
    default_title = _('Internal Server Error.')

    def __init__(self, title=None):
        if title is None:
            self.title = self.default_title
        else:
            self.title = title

    def __str__(self):
        return str(self.title)


# HTTP 400 - Bad Request
class BadRequest(APIException):
    status_code = status.BAD_REQUEST
    default_title = _('Malformed request.')


# HTTP 401 - Unauthorized
class AuthenticationFailed(APIException):
    status_code = status.UNAUTHORIZED
    default_title = _('Incorrect authentication credentials.')


# HTTP 401 - Unauthorized
class NotAuthenticated(APIException):
    status_code = status.UNAUTHORIZED
    default_title = _('Authentication credentials were not provided.')


# HTTP 403 - Forbidden
class Forbidden(APIException):
    status_code = status.FORBIDDEN
    default_title = _('You do not have permission to perform this action.')


# HTTP 404 - Not Found
class NotFound(APIException):
    status_code = status.NOT_FOUND
    default_title = _('Not found.')


# HTTP 405 - Method Not Allowed
class MethodNotAllowed(APIException):
    status_code = status.METHOD_NOT_ALLOWED
    default_title = _('Method "{method}" not allowed.')

    def __init__(self, method, title=None):
        if title is None:
            title = force_str(self.default_title).format(method=method)
        super().__init__(title)


# HTTP 406 - Not Acceptable
class NotAcceptable(APIException):
    status_code = status.NOT_ACCEPTABLE
    default_title = _('Could not satisfy the request Accept header.')


# HTTP 415 - Unsupported Media Type
class UnsupportedMediaType(APIException):
    status_code = status.UNSUPPORTED_MEDIA_TYPE
    default_title = _('Unsupported media type "{media_type}" in request.')


# HTTP 429 - Too Many Requests
class Throttled(APIException):
    status_code = status.TOO_MANY_REQUESTS
    default_title = _('Request was throttled.')
