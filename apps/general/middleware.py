# apps/general/middleware.py
from django.http import HttpResponsePermanentRedirect

class WWWRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0]
        if host == 'tropicalmovingsolutions.com':
            new_url = f"https://www.tropicalmovingsolutions.com{request.path}"
            return HttpResponsePermanentRedirect(new_url)
        return self.get_response(request)