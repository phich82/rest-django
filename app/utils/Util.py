from django.http import HttpRequest
from django.urls import reverse_lazy
from rest_framework.reverse import reverse

def exist_property(obj, key: str)-> bool:
    """ Check exists of specified property in object  """
    return getattr(obj, key, None)

def link(view_name, args=None, kwargs=None, request=None, **extra) -> str:
    """ Build url """
    return reverse(view_name, args=args, kwargs=kwargs, request=request, format=None, **extra)

def full_link(view_name, args=None, kwargs=None) -> str:
    """ Build full url (included host + port) """
    return  reverse_lazy(view_name, *args, **kwargs)

def parse_request(request: HttpRequest):
    """ Parse http request """

    query_params = {}

    for key in request.query_params.keys():
        query_params[key] = request.query_params.get(key)

    return {
        'headers': request.headers,
        'params': request.data,
        'query_params': query_params,
    }
