from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    """
    Middleware to require login for all pages except specified paths.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Paths allowed without login
        allowed_urls = [
            reverse('login'),  # Login page
            '/admin/login/',   # Django admin login
        ]

        if not request.user.is_authenticated and not any(request.path.startswith(url) for url in allowed_urls):
            return redirect('login')

        return self.get_response(request)


class AutoLogoutMiddleware:
    """
    Middleware to force logout after session expiry
    and redirect to login page.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs allowed without authentication
        allowed_urls = [
            reverse('login'),
            reverse('logout'),
            '/admin/login/',
            '/static/',  # allow static files
        ]

        # Allow static & media files
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)

        # Check authentication
        if not request.user.is_authenticated and not any(request.path.startswith(url) for url in allowed_urls):
            return redirect('login')

        return self.get_response(request)