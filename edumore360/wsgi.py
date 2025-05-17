"""
WSGI config for edumore360 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import environ

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()

from django.core.wsgi import get_wsgi_application

# Use production settings if specified in environment
settings_module = env('DJANGO_SETTINGS_MODULE', default='edumore360.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
