from rest_framework.reverse import reverse


def link(viewname, args=None, kwargs=None, request=None, format=None, **extra):
    return reverse(viewname, args=args, kwargs=kwargs, request=request, format=format, **extra)