# -*- coding: utf-8 -*-

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


class NotFound(APIException):
    status_code = status.NOT_FOUND
    default_title = _('Not found.')


class MethodNotAllowed(APIException):
    status_code = status.METHOD_NOT_ALLOWED
    default_detail = _('Method "{method}" not allowed.')
    default_code = 'method_not_allowed'

    def __init__(self, method, title=None):
        if title is None:
            title = force_str(self.default_title).format(method=method)
        super().__init__(title)
