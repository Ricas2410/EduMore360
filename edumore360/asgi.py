"""
ASGI config for edumore360 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import environ

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()

from django.core.asgi import get_asgi_application

# Use production settings if specified in environment
settings_module = env('DJANGO_SETTINGS_MODULE', default='edumore360.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_asgi_application()
