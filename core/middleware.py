"""
Middleware for SEO improvements.
"""
from django.http import HttpResponsePermanentRedirect


class CanonicalDomainMiddleware:
    """
    Middleware to ensure all requests use the canonical domain.
    Redirects from non-canonical domains to the canonical domain.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        """
        Process the request and redirect to canonical domain if needed.
        """
        host = request.get_host().lower()
        
        # Define your canonical domain here
        canonical_domain = 'edumore360.onrender.com'
        
        # Skip for local development
        if 'localhost' in host or '127.0.0.1' in host:
            return self.get_response(request)
            
        # Redirect to canonical domain if not already on it
        if host != canonical_domain:
            scheme = request.scheme
            path = request.get_full_path()
            new_url = f'{scheme}://{canonical_domain}{path}'
            return HttpResponsePermanentRedirect(new_url)
            
        return self.get_response(request)


class TrailingSlashMiddleware:
    """
    Middleware to ensure consistent URL format by adding trailing slashes.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        """
        Process the request and add trailing slash if needed.
        """
        # Skip for static files, media files, and admin
        if request.path.startswith('/static/') or request.path.startswith('/media/') or request.path.startswith('/admin/'):
            return self.get_response(request)
            
        # Skip for files with extensions
        if '.' in request.path.split('/')[-1]:
            return self.get_response(request)
            
        # Add trailing slash if not present
        if not request.path.endswith('/') and not request.path == '':
            scheme = request.scheme
            host = request.get_host()
            path = request.get_full_path()
            new_url = f'{scheme}://{host}{path}/'
            return HttpResponsePermanentRedirect(new_url)
            
        return self.get_response(request)
