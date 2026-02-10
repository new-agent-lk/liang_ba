"""
WSGI config for company project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Use production_settings in production, local_settings otherwise
if os.environ.get("DJANGO_SETTINGS_MODULE") == "production_settings":
    pass  # Already set by environment
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "local_settings")

application = get_wsgi_application()
