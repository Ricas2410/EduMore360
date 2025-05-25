import requests
import json
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.conf import settings
from .models import PageView, UserSession
from .utils import get_client_ip, parse_user_agent, get_location_from_ip


class AnalyticsMiddleware(MiddlewareMixin):
    """Middleware to track page views and user analytics."""
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def process_request(self, request):
        """Track page view on each request."""
        # Skip tracking for certain paths
        skip_paths = [
            '/admin/',
            '/static/',
            '/media/',
            '/favicon.ico',
            '/robots.txt',
            '/sitemap.xml',
            '/api/',  # Skip API calls
        ]
        
        # Skip if path should be ignored
        if any(request.path.startswith(path) for path in skip_paths):
            return None
        
        # Skip if it's an AJAX request (to avoid double counting)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return None
        
        # Get user information
        user = request.user if request.user.is_authenticated else None
        session_key = request.session.session_key
        
        # Get client information
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        referrer = request.META.get('HTTP_REFERER', '')
        
        # Parse user agent for device info
        device_info = parse_user_agent(user_agent)
        
        # Get location from IP (async in production)
        location_info = get_location_from_ip(ip_address)
        
        try:
            # Create page view record
            page_view = PageView.objects.create(
                user=user,
                session_key=session_key,
                path=request.path,
                page_title=self.get_page_title(request.path),
                referrer=referrer,
                ip_address=ip_address,
                user_agent=user_agent,
                country=location_info.get('country', ''),
                country_code=location_info.get('country_code', ''),
                city=location_info.get('city', ''),
                region=location_info.get('region', ''),
                device_type=device_info.get('device_type', ''),
                browser=device_info.get('browser', ''),
                operating_system=device_info.get('os', ''),
            )
            
            # Update or create user session
            if session_key:
                session, created = UserSession.objects.get_or_create(
                    session_key=session_key,
                    defaults={
                        'user': user,
                        'ip_address': ip_address,
                        'user_agent': user_agent,
                        'country': location_info.get('country', ''),
                    }
                )
                
                if not created:
                    # Update existing session
                    session.last_activity = timezone.now()
                    session.page_views += 1
                    session.save()
                else:
                    session.page_views = 1
                    session.save()
            
        except Exception as e:
            # Log error but don't break the request
            print(f"Analytics tracking error: {e}")
        
        return None
    
    def get_page_title(self, path):
        """Get a human-readable page title from the path."""
        title_map = {
            '/': 'Home',
            '/dashboard/': 'Dashboard',
            '/quiz/': 'Quizzes',
            '/notes/': 'Notes',
            '/profile/': 'Profile',
            '/subscription/': 'Subscription',
            '/about/': 'About',
            '/contact/': 'Contact',
        }
        
        # Check for exact matches first
        if path in title_map:
            return title_map[path]
        
        # Check for partial matches
        for route, title in title_map.items():
            if path.startswith(route):
                return title
        
        # Default title
        return 'Page'
