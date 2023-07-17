from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions, status
from rest_framework.views import exception_handler, set_rollback

from app.core import ApiResponse
from app.utils import Util


def custom_exception_handler(exception, context) -> ApiResponse:
    """Custom exception handler

    Args:
        exception (Http404 | PermissionDenied | APIException): Exception
        context (_type_): _description_

    Returns:
        ApiResponse: Api Response
    """

    print('==================')
    print(context)
    if Util.exist_property(context, 'view'):
        print(f'View => {context.view}')
    if Util.exist_property(context, 'request'):
        print(f'Request => {context.request}')
    print('==================')

    headers = {}
    status_code = status.HTTP_400_BAD_REQUEST

    if isinstance(exception, Http404):
        exception = exceptions.NotFound()

    elif isinstance(exception, PermissionDenied):
        exception = exceptions.PermissionDenied()
        
    if isinstance(exception, exceptions.ValidationError):
        print('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')

    if isinstance(exception, exceptions.APIException):
        if Util.exist_property(exception, 'auth_header'):
            headers['WWW-Authenticate'] = exception.auth_header
        if Util.exist_property(exception, 'wait'):
            headers['Retry-After'] = '%d' % exception.wait

        error_message = exception.detail
        # if isinstance(exception.detail, (list, dict)):
        #     error_message = exception.detail
        # else:
        #     error_message = exception.detail

        if Util.exist_property(exception, 'status_code'):
            status_code = exception.status_code

        set_rollback()

        return ApiResponse.error(error_message, status=status_code, headers=headers)

    return ApiResponse.error('Unknown error', status=status_code, headers=headers)
