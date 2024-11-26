"""
WSGI config for price_tracker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from tracker.checker import start_thread  # Import the thread starter
start_thread()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'price_tracker.settings')

application = get_wsgi_application()
