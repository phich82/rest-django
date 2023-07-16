def test(name=None, **kwargs):
    def decorator(func):
        func.name = name
        func.kwargs = kwargs
        return func
    return decorator