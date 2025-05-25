import requests
import json
from user_agents import parse
from django.core.cache import cache


def get_client_ip(request):
    """Get the real IP address of the client."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def parse_user_agent(user_agent_string):
    """Parse user agent string to extract device information."""
    try:
        user_agent = parse(user_agent_string)
        
        # Determine device type
        if user_agent.is_mobile:
            device_type = 'mobile'
        elif user_agent.is_tablet:
            device_type = 'tablet'
        else:
            device_type = 'desktop'
        
        return {
            'device_type': device_type,
            'browser': f"{user_agent.browser.family} {user_agent.browser.version_string}",
            'os': f"{user_agent.os.family} {user_agent.os.version_string}",
        }
    except Exception:
        return {
            'device_type': 'unknown',
            'browser': 'unknown',
            'os': 'unknown',
        }


def get_location_from_ip(ip_address):
    """Get location information from IP address using a free service."""
    # Skip for local/private IPs
    if ip_address in ['127.0.0.1', 'localhost'] or ip_address.startswith('192.168.') or ip_address.startswith('10.'):
        return {
            'country': 'Local',
            'country_code': 'LC',
            'city': 'Local',
            'region': 'Local',
        }
    
    # Check cache first
    cache_key = f"location_{ip_address}"
    cached_location = cache.get(cache_key)
    if cached_location:
        return cached_location
    
    try:
        # Use ipapi.co (free tier: 1000 requests/day)
        response = requests.get(f"https://ipapi.co/{ip_address}/json/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            location_info = {
                'country': data.get('country_name', ''),
                'country_code': data.get('country_code', ''),
                'city': data.get('city', ''),
                'region': data.get('region', ''),
            }
            
            # Cache for 24 hours
            cache.set(cache_key, location_info, 86400)
            return location_info
    except Exception as e:
        print(f"Error getting location for IP {ip_address}: {e}")
    
    # Fallback
    return {
        'country': 'Unknown',
        'country_code': 'UN',
        'city': 'Unknown',
        'region': 'Unknown',
    }


def get_country_flag_emoji(country_code):
    """Convert country code to flag emoji."""
    if not country_code or len(country_code) != 2:
        return '🌍'
    
    # Convert country code to flag emoji
    flag_offset = 0x1F1E6 - ord('A')
    flag = ''.join(chr(ord(char) + flag_offset) for char in country_code.upper())
    return flag


def aggregate_daily_stats(date):
    """Aggregate daily statistics for a given date."""
    from django.db.models import Count, Avg
    from .models import PageView, QuizAnalytics, DailyStats
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    # Get page view stats
    page_views = PageView.objects.filter(timestamp__date=date)
    total_page_views = page_views.count()
    unique_page_views = page_views.values('ip_address').distinct().count()
    
    # Get user stats
    total_users = User.objects.filter(date_joined__date__lte=date).count()
    new_users = User.objects.filter(date_joined__date=date).count()
    active_users = page_views.filter(user__isnull=False).values('user').distinct().count()
    
    # Get quiz stats
    quiz_analytics = QuizAnalytics.objects.filter(started_at__date=date)
    quizzes_started = quiz_analytics.count()
    quizzes_completed = quiz_analytics.filter(completed_at__isnull=False).count()
    average_score = quiz_analytics.filter(score__isnull=False).aggregate(Avg('score'))['score__avg']
    
    # Get top countries
    country_stats = (
        page_views
        .exclude(country='')
        .values('country', 'country_code')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )
    
    top_countries = {}
    for stat in country_stats:
        country = stat['country']
        country_code = stat['country_code']
        count = stat['count']
        flag = get_country_flag_emoji(country_code)
        top_countries[country] = {
            'count': count,
            'country_code': country_code,
            'flag': flag
        }
    
    # Create or update daily stats
    daily_stats, created = DailyStats.objects.get_or_create(
        date=date,
        defaults={
            'total_users': total_users,
            'new_users': new_users,
            'active_users': active_users,
            'total_page_views': total_page_views,
            'unique_page_views': unique_page_views,
            'quizzes_started': quizzes_started,
            'quizzes_completed': quizzes_completed,
            'average_score': average_score,
            'top_countries': top_countries,
        }
    )
    
    if not created:
        # Update existing record
        daily_stats.total_users = total_users
        daily_stats.new_users = new_users
        daily_stats.active_users = active_users
        daily_stats.total_page_views = total_page_views
        daily_stats.unique_page_views = unique_page_views
        daily_stats.quizzes_started = quizzes_started
        daily_stats.quizzes_completed = quizzes_completed
        daily_stats.average_score = average_score
        daily_stats.top_countries = top_countries
        daily_stats.save()
    
    return daily_stats
