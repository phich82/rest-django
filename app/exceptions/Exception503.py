from rest_framework.exceptions import APIException


class Exception503(APIException):
    """ Service Unavailable """
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'