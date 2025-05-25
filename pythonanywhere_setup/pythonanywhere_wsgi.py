# 🚀 EduMore360 PythonAnywhere WSGI Configuration
# This file contains the WSGI configuration for PythonAnywhere deployment

import os
import sys
from pathlib import Path

# Add your project directory to the sys.path
path = '/home/edumore360/EduMore360'
if path not in sys.path:
    sys.path.insert(0, path)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings_pythonanywhere')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

# Create the WSGI application
application = get_wsgi_application()

# Optional: Add error handling for better debugging
def application_with_error_handling(environ, start_response):
    try:
        return application(environ, start_response)
    except Exception as e:
        # Log the error
        import logging
        logging.error(f"WSGI Error: {str(e)}")
        
        # Return a simple error response
        status = '500 Internal Server Error'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [b'Internal Server Error. Please check the error logs.']

# Use the error handling wrapper in development
# For production, use the standard application
# application = application_with_error_handling
