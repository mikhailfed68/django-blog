"""Сontains common middleware for the entire project"""

from django.shortcuts import redirect
from django.utils.cache import patch_vary_headers


class RemoveEmptyQueryString:
    """
    If the incoming url has empty get parameters in the query string,
    the middleware removes it and redirects the request without empty params.
    """

    def __init__(self, get_response) -> None:
        self._get_response = get_response

    def __call__(self, request):
        querystring = request.GET.copy()
        empty_params = [param for param, value in querystring.items() if not value]

        for param in empty_params:
            del querystring[param]

        if request.GET != querystring:
            return redirect(f"{request.path_info}?{querystring.urlencode()}")
        return self._get_response(request)


class UpdateVaryForConditionalGetMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if hasattr(self, "process_template_response"):
            response = self.process_template_response(request, response)
        return response

    def process_template_response(self, request, response):
        if request.method != "GET":
            return response
        patch_vary_headers(response, ['If-None-Match', 'Etag'])
        print(response.headers)
        return response
