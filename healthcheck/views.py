"""
Health check views for the application.
These views are used to check if the application is running correctly.
"""

from django.http import HttpResponse

def health_check(request):
    """
    A very simple health check view that doesn't depend on any other parts of the application.
    This is used by Railway to check if the application is running.
    """
    return HttpResponse("OK", content_type="text/plain", status=200)
