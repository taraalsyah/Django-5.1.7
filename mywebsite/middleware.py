# mywebsite/middleware.py
from django.shortcuts import redirect
from django.urls import resolve, reverse
from django.conf import settings

class LoginRequiredMiddleware:
    """
    Middleware untuk memaksa login di semua halaman
    kecuali yang ada di whitelist.
    """

    # nama view yang boleh diakses tanpa login (url_name dari urls.py)
    EXEMPT_NAMES = [
        "/",
        "login",
        "logout",
        "register",
        "admin:login",  # kalau pakai admin django
        "verify_email",
        "google_redirect",
        "google_login_redirect",
        "socialaccount_login",
        "socialaccount_signup",
        "socialaccount_connections",
        "socialaccount_logout",
        "socialaccount_login_cancelled",
        "socialaccount_login_error",
        "socialaccount_email_verification_sent",
        "socialaccount_email_verification",
        "socialaccount_inactive",
        "admin",
        "landing_page"
    ]

    # path yang boleh diakses tanpa login
    EXEMPT_PATHS = [
        "/",
        "/login/",
        "/logout/",
        "/register/",
        "/admin/login/",
        "/verify/",
        "/accounts/",
        "/go-to-google-login/",
        "admin/",
        "/login/google/",
        "/accounts/google/login/",
        "/accounts/google/login/callback/",
        "/landing_page/",
    ]

    allowed_urls = [
    '/',
    '/login/',
    '/register/',
    '/static/',
    '/media/attachments/',
    '/verify/',
    '/accounts/',
    '/go-to-google-login/',
    '/login/google/',
    '/admin/login/',
    '/admin/',
    '/accounts/google/login/',
    '/accounts/google/login/callback/',
    '/landing_page/',
    ]


    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # jangan blokir request untuk static & media files
        if request.path.startswith(settings.STATIC_URL) or (
            hasattr(settings, "MEDIA_URL") and request.path.startswith(settings.MEDIA_URL)
        ):
            return self.get_response(request)

        # resolve url_name dari path yang diminta
        try:
            url_name = resolve(request.path_info).url_name
        except:
            url_name = None

        # cek apakah user belum login
        if not request.user.is_authenticated:
            if (
                request.path not in self.EXEMPT_PATHS
                and url_name not in self.EXEMPT_NAMES
            ):
                return redirect(settings.LOGIN_URL)

        return self.get_response(request)



class AutoLogoutMiddleware:


    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs allowed without authentication
        allowed_urls = [
        '/login/',
        '/register/',
        '/static/',
        '/media/',
        '/verify/',
        '/accounts/',
        '/go-to-google-login/',
        '/login/google/'
        '/admin/',
        '/admin/login/',
        '/verify-success/',
        '/verify-failed/',
        '/resend-verification/',
        '/media/attachments/',
        '/'
        ]

        # Allow static & media files
        if request.path.startswith('/static/') or request.path.startswith('/media/attachments/'):
            return self.get_response(request)

        # Check authentication
        if not request.user.is_authenticated and not any(request.path.startswith(url) for url in allowed_urls):
            return redirect('login')

        return self.get_response(request)
