"""
Minimal health check views.
These views are completely standalone and don't depend on any other part of the application.
"""

from django.http import HttpResponse

def health(request):
    """
    A minimal health check view that doesn't depend on any other part of the application.
    """
    return HttpResponse("OK", content_type="text/plain", status=200)
