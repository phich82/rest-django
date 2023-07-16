
# Define a middleware funtion
def my_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print("my_middleware => start")
        response = get_response(request)
        print("my_middleware => end")
        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware
