"""
Hybrid WSGI application for Railway deployment.
This application combines a minimal health check with the full Django application.
"""

import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Minimal health check application
def minimal_app(environ, start_response):
    """
    A minimal WSGI application that only serves the health check endpoint.
    """
    path = environ.get('PATH_INFO', '')

    if path == '/health/' or path == '/health':
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [b'OK']

    # For any other path, return a 404
    status = '404 Not Found'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    return [b'Not Found - Minimal App Only']

# Try to import the Django application
django_app = None
try:
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings_prod')

    # Add the project directory to the Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    # Import Django WSGI application
    from django.core.wsgi import get_wsgi_application
    django_app = get_wsgi_application()

    logger.info("Successfully loaded Django application with settings_prod")
except Exception as e:
    logger.error(f"Error loading Django application with settings_prod: {e}")
    logger.error("Trying with minimal settings...")

    try:
        # Try with minimal settings
        os.environ['DJANGO_SETTINGS_MODULE'] = 'edumore360.settings_minimal'

        # Import Django WSGI application
        from django.core.wsgi import get_wsgi_application
        django_app = get_wsgi_application()

        logger.info("Successfully loaded Django application with settings_minimal")
    except Exception as e:
        logger.error(f"Error loading Django application with settings_minimal: {e}")
        logger.error("Falling back to minimal health check application")

# Hybrid application
def application(environ, start_response):
    """
    A hybrid WSGI application that serves the health check endpoint
    and delegates other requests to the Django application if available.
    """
    path = environ.get('PATH_INFO', '')

    # Always handle health check with the minimal app
    if path == '/health/' or path == '/health':
        return minimal_app(environ, start_response)

    # If Django app is available, delegate to it
    if django_app:
        try:
            return django_app(environ, start_response)
        except Exception as e:
            logger.error(f"Error in Django application: {e}")
            # Fall back to minimal app on error
            return minimal_app(environ, start_response)

    # If Django app is not available, use minimal app
    return minimal_app(environ, start_response)

# If this file is run directly, start a simple server
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    port = 8000
    httpd = make_server('', port, application)
    print(f"Serving on port {port}...")
    httpd.serve_forever()
