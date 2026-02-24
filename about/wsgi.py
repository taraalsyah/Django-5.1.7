import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'Django-5.1.7.settings'
)

application = get_wsgi_application()