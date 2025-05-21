"""
WSGI config for edumore360 project on Render.
It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
import sys
from pathlib import Path

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings_render')

# Import the get_wsgi_application function
from django.core.wsgi import get_wsgi_application

# Get the WSGI application
application = get_wsgi_application()
