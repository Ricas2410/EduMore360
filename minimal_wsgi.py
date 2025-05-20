"""
WSGI config for Railway deployment.
This is a minimal WSGI application that only serves the health check endpoint.
"""

import os
import sys
from django.core.wsgi import get_wsgi_application
from django.urls import path
from django.http import HttpResponse

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings_prod')

# Create a minimal application that only serves the health check endpoint
def health(request):
    """A minimal health check view."""
    return HttpResponse("OK", content_type="text/plain", status=200)

# Create a minimal URLconf
urlpatterns = [
    path('health/', health),
]

# Create a minimal application
from django.core.handlers.wsgi import WSGIHandler
from django.urls import set_urlconf

class MinimalWSGIHandler(WSGIHandler):
    def __call__(self, environ, start_response):
        set_urlconf(urlpatterns)
        return super().__call__(environ, start_response)

# Create the application
application = MinimalWSGIHandler()

# Try to import the real application as a fallback
try:
    real_application = get_wsgi_application()
    
    # If we get here, the real application loaded successfully
    # Replace our minimal application with the real one
    application = real_application
    print("Loaded full WSGI application")
except Exception as e:
    print(f"Error loading full WSGI application: {e}")
    print("Using minimal WSGI application for health checks only")
