import re

from django.conf import settings
from django.shortcuts import redirect

class RequireLoginMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')

        if not request.user.is_authenticated():
            if True:
                return redirect(settings.LOGIN_URL)
    # def process_view(self, request, view_func, view_args, view_kwargs):
    #     # No need to process URLs if user already logged in
    #     if request.user.is_authenticated():
    #         return None

    #     # An exception match should immediately return None
    #     for url in self.exceptions:
    #         if url.match(request.path):
    #             return None

    #     # Requests matching a restricted URL pattern are returned
    #     # wrapped with the login_required decorator
    #     for url in self.required:
    #         if url.match(request.path):
    #             return login_required(view_func)(request, *view_args, **view_kwargs)

    #     # Explicitly return None for all non-matching requests
    #     return None